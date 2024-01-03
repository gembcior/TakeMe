function successResourceAction () {
  // window.location.href = window.location.origin
}

function test1 () {
  const data = {
    action: "take",
    resource_name : "PC-RESOURCE-01"
  }
  const dataToSend = JSON.stringify(data);
  const url = window.location.origin + "/api/resource"

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
