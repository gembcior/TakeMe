function successResourceAction () {
  window.location.href = window.location.origin
}

function takeResource (name) {
  const data = {
    cmd: "take",
    name : name
  }
  const dataToSend = JSON.stringify(data);
  const url = window.location.origin + "/resource"

  $.ajax({
    type: "POST",
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

function releaseResource (name) {
  const data = {
    cmd: "release",
    name : name
  }
  const dataToSend = JSON.stringify(data);
  const url = window.location.origin + "/resource"

  $.ajax({
    type: "POST",
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
