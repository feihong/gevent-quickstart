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

function log(data) {
  let output = $('#output')
  let para = $('<p>').text(data.value).appendTo(output)
  para.css('color', getColor(data.src))
  output.scrollTop(para.offset().top - output.offset().top + output.scrollTop())
}

let socket = new WebSocket('ws://' + location.host + '/echo')
socket.onopen = () => socket.send('Hello Websocket!')

socket.onmessage = evt => {
  let data = JSON.parse(evt.data)
  log(data)
}

$('button.task').on('click', () => {
  $.get('/start-task', data => console.log(data))
})

$('button.info').on('click', () => {
  $.getJSON('/get-info', data => {
    for (let [key, val] of Object.entries(data)) {
      log({value: `${key}: ${val}`, src: 'info'})
    }
  })
})

$('button.beat').on('click', () => {
  $.get('/toggle-beat', data => console.log(data))
})
