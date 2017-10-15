$('form').on('submit', evt => {
  evt.preventDefault()
  let input = $('input')
  socket.send(input.val())
  input.val('')
})

let socket = new WebSocket('ws://' + location.host + '/echo')
socket.onopen = () => socket.send('Hello Websocket!')

socket.onmessage = evt => {
  let output = $('#output')
  let para = $('<p>').text(evt.data).appendTo(output)
  output.scrollTop(para.offset().top - output.offset().top + output.scrollTop())
}

$('button').on('click', () => {
  $.get('/start-task', data => console.log(data))
})
