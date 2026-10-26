# Template — Refatoração

Use para reorganizar código existente sem alterar o comportamento externo.

---

## Template

```
## Contexto
Arquivo a refatorar: [ex: app/services/auth.py]
Problema atual: [por que precisa ser refatorado — dívida técnica, acoplamento, tamanho]
Arquitetura alvo: [ex: Repository Pattern, separação de responsabilidades, injeção de dependência]

## Código atual
[cole o código a ser refatorado]

## Instrução
Refatore o código acima para [objetivo específico].
O comportamento externo deve ser idêntico ao original.

## Formato
- Mostre o código refatorado completo (não diff)
- Se criar novos arquivos, liste-os com o caminho completo

## Critério de não-regressão
[cole os testes existentes que devem continuar passando sem modificação]

## Restrições
- A interface pública de [classe/função] não deve mudar
- Os testes listados acima devem passar sem nenhuma modificação
- Não adicione features novas — apenas reorganize o que existe
- [restrições específicas do projeto]
```

---

## Exemplo preenchido — extrair AuthRepository de AuthService

```
## Contexto
Arquivo a refatorar: app/services/auth.py
Problema atual: AuthService tem 180 linhas misturando lógica de negócio (validar credenciais,
gerar token) com queries diretas ao banco (SELECT FROM users WHERE email = ?).
Isso dificulta testar a lógica sem banco de dados.
Arquitetura alvo: Repository Pattern — UserRepository isola todas as queries.

## Código atual
class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, email: str, password: str) -> str:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_token(str(user.id))

    def logout(self, token: str) -> None:
        payload = verify_token(token)
        jti = payload["jti"]
        exp = payload["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())
        redis.setex(f"blocklist:{jti}", ttl, "1")

## Instrução
Refatore AuthService para usar um UserRepository que isola as queries ao banco.
AuthService não deve mais receber `db: Session` diretamente — receberá UserRepository.

## Formato
Dois arquivos:
- app/repositories/user_repository.py — UserRepository com interface AbstractUserRepository
- app/services/auth.py — AuthService refatorado recebendo UserRepository via construtor

## Critério de não-regressão
Os seguintes testes devem passar sem modificação após a refatoração:

def test_login_com_credenciais_validas(auth_service, usuario_fixture):
    token = auth_service.login("joao@example.com", "senha123")
    assert token is not None

def test_login_credenciais_invalidas(auth_service):
    with pytest.raises(InvalidCredentialsError):
        auth_service.login("nao@existe.com", "qualquer")

## Restrições
- A interface pública de AuthService (login, logout) não deve mudar
- Os testes acima devem passar sem nenhuma modificação
- Não adicione endpoints ou rotas
- Não altere o esquema do banco de dados
- Não adicione features de logging ou métricas
```

---

## Checklist antes de enviar um prompt de refatoração

- [ ] Você especificou o comportamento que deve ser preservado?
- [ ] Você listou os testes que não podem mudar?
- [ ] Você definiu o que está fora do escopo?
- [ ] A instrução tem uma meta específica (Repository Pattern? Separar responsabilidades? Reduzir tamanho?)?

Refatoração sem critério de não-regressão é o anti-padrão mais comum neste tipo de prompt — o modelo pode entregar código "mais limpo" que quebra os testes existentes.