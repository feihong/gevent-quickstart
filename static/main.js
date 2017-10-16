$('form').on('submit', evt => {
  evt.preventDefault()
  let input = $('input')
  socket.send(input.val())
  input.val('')
})

let niceColors = randomColor({luminosity: 'light', count: 30})
let colorMap = {}

function getColor(source) {
  if (source in colorMap) {
    return colorMap[source]
  } else {
    let color = niceColors.pop()
    colorMap[source] = color
    return color
  }
}

let socket = new WebSocket('ws://' + location.host + '/echo')
socket.onopen = () => socket.send('Hello Websocket!')

socket.onmessage = evt => {
  let output = $('#output')
  let data = JSON.parse(evt.data)
  let para = $('<p>').text(data.value).appendTo(output)
  para.css('color', getColor(data.src))
  output.scrollTop(para.offset().top - output.offset().top + output.scrollTop())
}

$('button.task').on('click', () => {
  $.get('/start-task', data => console.log(data))
})

$('button.info').on('click', () => {
  $.getJSON('/get-info', data => console.log(data))
})

$('button.beat').on('click', () => {
  $.get('/toggle-beat', data => console.log(data))
})
