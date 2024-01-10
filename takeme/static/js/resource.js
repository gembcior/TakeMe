function successResourceAction () {
  window.location.href = window.location.origin
}


function takeResource (id) {
  const url = window.location.origin + "/resource/take/" + id

  $.ajax({
    type: "POST",
    url: url,
    data: "",
    success: successResourceAction,
    dataType: "text",
  });
}


function releaseResource (id) {
  const url = window.location.origin + "/resource/release/" + id

  $.ajax({
    type: "POST",
    url: url,
    data: "",
    success: successResourceAction,
    dataType: "",
  });
}


function setResourceMsg (id, msg) {
  const data = {
    cmd: "msg",
    data : msg
  }
  const dataToSend = JSON.stringify(data);
  const url = window.location.origin + "/resource/msg/" + id

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


function update_resource_content(id, content) {
  const url = window.location.origin + "/resource/list/" + id

  $.get(url, function(data, status){
    const item = document.getElementById(`resource${id}ListItem`)
    const info = document.getElementById(`collapseResource${id}Info`)
    const collapseValue = info.classList.value
    var html = $($.parseHTML(data));
    html.find(`#collapseResource${id}Info`).removeClass().addClass(collapseValue)
    $( item ).replaceWith(html)
  });
}


$(document).ready(function() {
  var socket = io();
  socket.connect();

  socket.on('after connect', function(data) {
  });

  socket.on("resource update", function(data) {
    const id = data.resource_id
    const content = data.content
    console.log(`Resource ${id} update`)
    update_resource_content(id, content)
  })

  socket.on("resource no update", function(data) {
  })
});
