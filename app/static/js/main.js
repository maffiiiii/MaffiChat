const flashlight = document.querySelector('.flashlight');
let timeoutId;

document.addEventListener('mousemove', e => {
  flashlight.style.left = `${e.clientX}px`;
  flashlight.style.top = `${e.clientY}px`;
  flashlight.style.opacity = '1';  

  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    flashlight.style.opacity = '0';  
  }, 1000);
});

document.addEventListener('mouseleave', () => {
  flashlight.style.opacity = '0';  
});

