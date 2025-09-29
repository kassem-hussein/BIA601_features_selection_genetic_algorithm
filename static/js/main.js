let dargzone = document.getElementById('dropzone')
const fileInput = document.getElementById('fileInput');
let selected_file = document.getElementById('selected-file')
let open_nav      = document.getElementById('open_nav')
let close_nav     = document.getElementById('close_nav')
let mobile_nav    = document.getElementById('mobile_nav')


let lastScrollY = window.scrollY;
const header = document.getElementsByTagName('header')[0];

window.addEventListener('scroll', () => {
  if (window.innerWidth < 768) return;
  const currentScrollY = window.scrollY;
  
  if (currentScrollY > lastScrollY && currentScrollY > 100) {
    // Scrolling down
    header.classList.add('-translate-y-full');
  } else if (currentScrollY < lastScrollY) {
    // Scrolling up
    header.classList.remove('-translate-y-full');
  }

  lastScrollY = currentScrollY;
});



open_nav.addEventListener('click',()=>{
      document.body.classList.add('overflow-hidden')
      mobile_nav.classList.remove('hidden')
      mobile_nav.classList.add('flex')
})
close_nav.addEventListener('click',()=>{
      document.body.classList.remove('overflow-hidden')
      mobile_nav.classList.remove('flex')
      mobile_nav.classList.add('hidden')
})

dargzone.addEventListener('click',()=>fileInput.click())
dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('bg-blue-100');
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('bg-blue-100');
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('bg-blue-100');
    fileInput.files = e.dataTransfer.files;
    selected_file.innerHTML= `selected file is ${fileInput.files[0].name}`

  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      console.log('jere')
      selected_file.innerText =  `selected file is ${fileInput.files[0].name}`;
    }
  });


