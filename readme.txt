# Cifra de Vigenere
# Rodrigo Teixeira Soares 	19/0019760

Execução do trabalho:

Instalar Python 3.9 ou acima e executar o seguinte comando na pasta do projeto:

python3 vigenere.py [operation] input.txt key.txt output.txt [language]

operation:
c -> cifrar texto do input.txt para o output.txt usando a chave em key.txt
d -> decifrar texto do input.txt para o output.txt usando a chave em key.txt
b -> quebrar (break) a cifra do input.txt. Caso o usuário confirme que a mensagem foi decifrada, salvar a chave encontrada em key.txt e o texto decifrado em output.txt

language [opcional]:
ptbr -> quebrar o código usando a frequencia de letras da lingua portuguesa. Esta é a opção padrão caso o usuário não coloque esse argumento.
en -> quebrar o código usando a frequencia de letras da lingua inglesa.

exemplo:

python3 vigenere.py b cyphered.txt key.txt decyphered.txt en


