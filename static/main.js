$('form').on('submit', evt => {
  evt.preventDefault()
  let input = $('input')
  socket.send(input.val())
  input.val('')
})

let socket = new WebSocket('ws://' + location.host + '/echo')
socket.onopen = () => socket.send('Hello Websocket!')

socket.onmessage = evt => {
  console.log(evt.data)
  $('<p>').text(evt.data).appendTo('#results')
}
