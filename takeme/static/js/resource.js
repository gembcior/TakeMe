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


function deleteResource (id) {
  const url = window.location.origin + "/resource/rm/" + id

  $.ajax({
    type: "POST",
    url: url,
    data: "",
    success: successResourceAction,
    dataType: "",
  });
}


$(document).ready(function() {
  document.querySelectorAll('time').forEach($e => {
    const userLocale = navigator.languages && navigator.languages.length ? navigator.languages[0] : navigator.language;
    const date = new Date($e.dateTime);
    $e.innerHTML = date.toLocaleString(userLocale, { hour12: false });
  });
});
