function successResourceAction () {
  window.location.href = window.location.origin
}

// function takeResource (name) {
//   const data = {
//     cmd: "take",
//     name : name
//   }
//   const dataToSend = JSON.stringify(data);
//   const url = window.location.origin + "/resource"

//   $.ajax({
//     type: "POST",
//     url: url,
//     data: dataToSend,
//     success: successResourceAction,
//     dataType: "json",
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//   });
// }

function takeResource (name) {
  const url = window.location.origin + "/resource/take/" + name

  $.ajax({
    type: "POST",
    url: url,
    data: "",
    success: successResourceAction,
    dataType: "text",
  });
}

function releaseResource (name) {
  const url = window.location.origin + "/resource/release/" + name

  $.ajax({
    type: "POST",
    url: url,
    data: "",
    success: successResourceAction,
    dataType: "",
  });
}

function setResourceMsg (name, msg) {
  const data = {
    cmd: "msg",
    data : msg
  }
  const dataToSend = JSON.stringify(data);
  const url = window.location.origin + "/resource/msg/" + name

  $.ajax({
    type: "PUT",
    url: url,
    data: dataToSend,
    success: successResourceAction,
    dataType: "json",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
}

const messageModal = document.getElementById('messageModal')
if (messageModal) {
  messageModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const recipient = button.getAttribute('data-bs-resource')
    const modalTitle = messageModal.querySelector('#messageModalLabel')
    const modalSubmit = messageModal.querySelector('#setMsgModalButton')

    modalTitle.textContent = `Set message for ${recipient}`
    modalSubmit.setAttribute('data-bs-resource', recipient)
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

      const recipient = messageSetButton.getAttribute('data-bs-resource')
      const messageText = messageModal.querySelector('#messageText')
      $('#messageModal').modal('hide');
      setResourceMsg(recipient, messageText.value)
    })
  }
}

$(document).ready(function() {
  var socket = io.connect();

  socket.on('after connect', function(msg) {
  });

  socket.on("resource update", function() {
    location.reload()
  })
});
