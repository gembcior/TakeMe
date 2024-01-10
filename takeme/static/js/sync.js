function update_resource_content(id) {
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
    console.log(`Resource ${id} update`)
    update_resource_content(id)
  })

  socket.on("resource no update", function(data) {
  })

  socket.on("all resource update", function() {
    console.log("Update all resources")
    location.reload()
  })
});
