const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'white'; // Set canvas background to white
ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill canvas with white background

let drawing = false;
let lastX, lastY;
let rubberMode = false;
let penSize = 10;

canvas.addEventListener('mousedown', (e) => {
  drawing = true;
  lastX = e.offsetX;
  lastY = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
  if (drawing) {
    ctx.lineWidth = penSize * 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    if (rubberMode) {
      ctx.strokeStyle = 'white'; // Erase with white
    } else {
      ctx.strokeStyle = 'black'; // Draw black lines
    }
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    lastX = e.offsetX;
    lastY = e.offsetY;
  }
});

canvas.addEventListener('mouseup', () => {
  drawing = false;
});


document.getElementById('send-btn').addEventListener('click', () => {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/send', true);
  xhr.responseType = 'blob'; // Set response type to blob
  xhr.setRequestHeader('Content-Type', 'application/json');

  const imageData = canvas.toDataURL('image/jpeg');
  const jsonData = { image: imageData };
  xhr.send(JSON.stringify(jsonData));

  // Show the video container
  document.getElementById('canvas').style.display = 'none';
  document.getElementById('video-container').style.display = 'block';

  // Create an img element
  const img = document.getElementById('video-feed');

  img.src = '/video_feed?' + new Date().getTime();

  img.onload = () => {
    // Wait for 1 second to ensure the video has ended
    setTimeout(() => {
      // Display the canvas again with the last frame
      document.getElementById('canvas').style.display = 'block';
      document.getElementById('video-container').style.display = 'none';

      // Make an AJAX request to get the last frame
      const xhr = new XMLHttpRequest();
      xhr.open('GET', '/last_frame', true);
      xhr.responseType = 'text'; // Get the response as text
      xhr.onload = () => {
        if (xhr.status === 200) {
          const lastFrameImg = new Image();
          lastFrameImg.onload = () => {
            // Draw the last frame onto the canvas
            ctx.drawImage(lastFrameImg, 0, 0, canvas.width, canvas.height);
          };
          lastFrameImg.src = xhr.responseText; // Update the src attribute with the base64 encoded image string
        }
      };
      xhr.send();
    }, 1000); // wait for 1 second
  };
});

document.getElementById('rubber-btn').addEventListener('click', () => {
  rubberMode = !rubberMode;
  if (rubberMode) {
    document.getElementById('rubber-btn').classList.add('active');
  } else {
    document.getElementById('rubber-btn').classList.remove('active');
  }
});

document.getElementById('clear-btn').addEventListener('click', () => {
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
});

document.getElementById('size-slider').addEventListener('input', (e) => {
  penSize = e.target.value;
});