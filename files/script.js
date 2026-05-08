// Botão WhatsApp/Chatbot — abre o Typebot configurado
const botao = document.getElementById('whatsapp-button');
if (botao) {
  botao.addEventListener('click', () => {
    // Troque pela URL do seu Typebot aqui
    window.open('https://typebot.io', '_blank');
  });
}
