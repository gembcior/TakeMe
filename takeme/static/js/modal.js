$(document).ready(function() {
  const messageModal = document.getElementById('messageModal')
  if (messageModal) {
    messageModal.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget
      const recipient = button.getAttribute('data-bs-resource')
      const recipientId = button.getAttribute('data-bs-resource-id')
      const modalTitle = messageModal.querySelector('#messageModalLabel')
      const modalSubmit = messageModal.querySelector('#setMsgModalButton')

      modalTitle.textContent = `Set message for ${recipient}`
      modalSubmit.setAttribute('data-bs-resource', recipient)
      modalSubmit.setAttribute('data-bs-resource-id', recipientId)
    })

    messageModal.addEventListener('hidden.bs.modal', event => {
      const modalTitle = messageModal.querySelector('#messageModalLabel')
      const modalSubmit = messageModal.querySelector('#setMsgModalButton')

      modalTitle.textContent = 'Set message'
      modalSubmit.setAttribute('data-bs-resource', "")
    })

    const messageSetButton = document.getElementById('setMsgModalButton')
    if (messageSetButton) {
      messageSetButton.addEventListener('click', function() {

        const recipientId = messageSetButton.getAttribute('data-bs-resource-id')
        const messageText = messageModal.querySelector('#messageText')
        $('#messageModal').modal('hide');
        setResourceMsg(recipientId, messageText.value)
      })
    }
  }
});
