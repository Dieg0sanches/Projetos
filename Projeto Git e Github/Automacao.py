from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests


def _obter_sitekey_recaptcha(driver):
    """Tenta extrair o sitekey do reCAPTCHA v2 presente na página."""
    sitekey = None
    try:
        # Tentativa 1: div padrão do reCAPTCHA
        el = driver.find_element(By.CSS_SELECTOR, '.g-recaptcha')
        sitekey = el.get_attribute('data-sitekey')
    except Exception:
        pass
    if not sitekey:
        try:
            # Tentativa 2: qualquer elemento com data-sitekey
            el = driver.find_element(By.CSS_SELECTOR, '[data-sitekey]')
            sitekey = el.get_attribute('data-sitekey')
        except Exception:
            pass
    return sitekey


def _resolver_recaptcha_v2_com_2captcha(driver, page_url, api_key, timeout=180, poll_interval=5):
    """
    Resolve reCAPTCHA v2 usando o serviço 2Captcha e injeta o token na página.
    Retorna True em caso de sucesso, False caso contrário.
    """
    if not api_key:
        print("Chave da API do 2Captcha não fornecida. Pulando resolução automática.")
        return False

    sitekey = _obter_sitekey_recaptcha(driver)
    if not sitekey:
        print("Nenhum reCAPTCHA (sitekey) foi encontrado na página.")
        return False

    print(f"reCAPTCHA detectado. Iniciando solução via 2Captcha... (sitekey={sitekey})")

    try:
        # Enviar o captcha para solução
        in_payload = {
            'key': api_key,
            'method': 'userrecaptcha',
            'googlekey': sitekey,
            'pageurl': page_url,
            'json': 1,
        }
        r = requests.post('http://2captcha.com/in.php', data=in_payload, timeout=30)
        r.raise_for_status()
        rj = r.json()
        if rj.get('status') != 1:
            print(f"2Captcha retornou erro ao enviar: {rj}")
            return False
        request_id = rj.get('request')

        # Aguardar a solução ficando pronta
        print("Aguardando a solução do 2Captcha...")
        deadline = time.time() + timeout
        token = None
        while time.time() < deadline:
            time.sleep(poll_interval)
            res = requests.get('http://2captcha.com/res.php', params={
                'key': api_key,
                'action': 'get',
                'id': request_id,
                'json': 1,
            }, timeout=30)
            res.raise_for_status()
            rj = res.json()
            if rj.get('status') == 1:
                token = rj.get('request')
                break
            elif rj.get('request') != 'CAPCHA_NOT_READY':
                print(f"Erro do 2Captcha durante polling: {rj}")
                return False

        if not token:
            print("Tempo esgotado esperando a solução do 2Captcha.")
            return False

        # Injetar o token no campo g-recaptcha-response
        js = (
            "var d=document.getElementById('g-recaptcha-response');"
            "if(!d){d=document.createElement('textarea');d.id='g-recaptcha-response';d.name='g-recaptcha-response';d.style.display='none';document.body.appendChild(d);}"
            "d.value=arguments[0];"
        )
        driver.execute_script(js, token)
        print("Token do reCAPTCHA injetado com sucesso.")
        return True
    except Exception as e:
        print(f"Falha ao resolver reCAPTCHA via 2Captcha: {e}")
        return False


def _salvar_screenshot_site(driver, caminho_arquivo, full_page=True):
    """
    Salva um screenshot da página atual.
    - Garante que o diretório de destino exista.
    - Tenta capturar a página inteira (full page) redimensionando a janela para o
      tamanho total do documento; caso não seja possível, faz screenshot do viewport.
    Retorna True/False indicando sucesso.
    """
    try:
        # Garante a existência do diretório
        dirn = os.path.dirname(caminho_arquivo)
        if dirn and not os.path.exists(dirn):
            os.makedirs(dirn, exist_ok=True)

        if full_page:
            # Guarda o tamanho original
            try:
                original_size = driver.get_window_size()
                total_width = driver.execute_script(
                    "return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth, document.documentElement.clientWidth);"
                )
                total_height = driver.execute_script(
                    "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.documentElement.clientHeight);"
                )
                # Limita tamanho máximo razoável para evitar erros em páginas muito longas
                total_width = min(int(total_width or 1920), 10000)
                total_height = min(int(total_height or 1080), 20000)
                driver.set_window_size(total_width, total_height)
                ok = driver.save_screenshot(caminho_arquivo)
                # Restaura janela
                if isinstance(original_size, dict) and 'width' in original_size and 'height' in original_size:
                    driver.set_window_size(original_size['width'], original_size['height'])
                return ok
            except Exception:
                # Fallback para screenshot simples do viewport
                return driver.save_screenshot(caminho_arquivo)
        else:
            return driver.save_screenshot(caminho_arquivo)
    except Exception as e:
        try:
            # Último fallback usando API alternativa do Selenium
            return driver.get_screenshot_as_file(caminho_arquivo)
        except Exception:
            print(f"Falha ao salvar screenshot em '{caminho_arquivo}': {e}")
            return False


def automatizar_login_e_screenshot(url, usuario, senha, nome_arquivo, captcha_api_key=None):
    """
    Função para automatizar o login em um site, tirar uma captura de tela
    e salvar em um arquivo.

    Se 'captcha_api_key' for fornecida (ou variável de ambiente CAPTCHA_API_KEY estiver definida),
    o script tentará resolver automaticamente reCAPTCHA v2 via 2Captcha.
    Caso contrário, manterá a pausa para resolução manual.
    """
    # Permitir configuração via variável de ambiente
    captcha_api_key = captcha_api_key or os.getenv('CAPTCHA_API_KEY')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        driver.get(url)

        try:
            botao_cookies = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            botao_cookies.click()
            print("Banner de cookies aceito.")
        except Exception:
            print("Banner de cookies não encontrado ou já aceito.")

        campo_usuario = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//html/body/form/div/div[2]/div[2]/input[1]'))
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_senha = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[2]/input[2]')
        campo_senha.clear()
        campo_senha.send_keys(senha)

        # Resolver reCAPTCHA automaticamente quando possível
        solved = _resolver_recaptcha_v2_com_2captcha(driver, url, captcha_api_key)
        if not solved:
            # Fallback manual
            print("\n!!! ATENÇÃO !!!")
            print("Se houver reCAPTCHA, você tem 15 segundos para resolvê-lo manualmente na janela do navegador.")
            time.sleep(15)

        botao_login = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[2]/button')
        botao_login.click()

        print("Aguardando confirmação de login...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Minha Conta")]'))
        )
        print("Login realizado com sucesso!")

        _salvar_screenshot_site(driver, nome_arquivo)
        print(f"Captura de tela da página logada salva como '{nome_arquivo}'")

    except Exception as e:
        print(f"\nOcorreu um erro durante a automação: Login falhou ou o elemento de confirmação não foi encontrado.")
        print(f"Detalhe do erro: {str(e)}")
        try:
            _salvar_screenshot_site(driver, "erro_screenshot.png")
            print("Uma captura de tela do erro foi salva como 'erro_screenshot.png'")
        except Exception:
            pass

    finally:
        driver.quit()


if __name__ == "__main__":
    URL_LOGIN = "https://intranet.ctism.ufsm.br/cadastrousuario/logintest.html"
    USUARIO_EXEMPLO = "teste@teste.com.br"
    SENHA_EXEMPLO = "sua_senha_segura"
    NOME_ARQUIVO_SCREENSHOT = "screenshot_intrateste.png"

    # Você pode definir a variável de ambiente CAPTCHA_API_KEY ou passar diretamente abaixo
    CAPTCHA_API_KEY = os.getenv('CAPTCHA_API_KEY') or None  # substitua por sua chave se quiser testar agora

    automatizar_login_e_screenshot(URL_LOGIN, USUARIO_EXEMPLO, SENHA_EXEMPLO, NOME_ARQUIVO_SCREENSHOT, CAPTCHA_API_KEY)
