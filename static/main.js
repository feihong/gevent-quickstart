$('form').on('submit', evt => {
  evt.preventDefault()
  let input = $('input')
  socket.send(input.val())
  input.val('')
})

let socket = new WebSocket('ws://' + location.host + '/echo')
socket.onopen = () => socket.send('Hello Websocket!')

socket.onmessage = evt => {
  $('<p>').text(evt.data).appendTo('#results')
}

$('button').on('click', () => {
  $.get('/start-task', data => console.log(data))
})
