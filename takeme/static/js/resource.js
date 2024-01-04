function successResourceAction () {
  window.location.href = window.location.origin
}

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
