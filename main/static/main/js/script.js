const canvas = document.getElementById("gridCanvas");
const ctx = canvas.getContext("2d");

let width = (canvas.width = window.innerWidth);
let height = (canvas.height = window.innerHeight);

const gridSize = 60; // size of boxes
const gridColor = "rgba(200, 200, 200, 0.25)"; // light gray lines, medium visibility

function drawGrid() {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 1;

    // Vertical lines
    for (let x = 0; x <= width; x += gridSize) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
    }

    // Horizontal lines
    for (let y = 0; y <= height; y += gridSize) {
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
    }

    ctx.stroke();
}

// Draw once (static, no animation)
drawGrid();

// Redraw grid when window resizes
window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    drawGrid();
});

// Typing Animation
const typingElement = document.getElementById('typing');
const text = typingElement.getAttribute("data-text");  // fetch from Django
let index = 0;

function type() {
    if (index < text.length) {
        typingElement.innerHTML += text.charAt(index);
        index++;
        setTimeout(type, 150);
    } else {
        typingElement.classList.add('finished');
    }
}

// Start typing animation
setTimeout(type, 500);

// Counter Animation
const counters = document.querySelectorAll('.counter-number');
const duration = 2000; // 2s animation

function animateCounter(counter) {
    const target = +counter.getAttribute('data-target');
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const value = Math.floor(progress * target);
        counter.innerText = value;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// Start counter animation when in view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.querySelectorAll('.counter-number').forEach(animateCounter);
            observer.unobserve(entry.target); // run only once
        }
    });
}, { threshold: 0.5 });

observer.observe(document.querySelector('.counters'));

// Timeline Tabs
const timelineButtons = document.querySelectorAll('.timeline-btn');
const timelineSections = document.querySelectorAll('.timeline-section');
let timeouts = []; // store timeouts

// Animate default active section
document.querySelectorAll('.timeline-section.active .timeline-item')
    .forEach((item, index) => {
        const t = setTimeout(() => item.classList.add('visible'), index * 200);
        timeouts.push(t);
    });

// Click event
timelineButtons.forEach(button => {
    button.addEventListener('click', () => {
        const target = button.getAttribute('data-target');

        // Clear any pending animations
        timeouts.forEach(t => clearTimeout(t));
        timeouts = [];

        // Update active button
        timelineButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Show corresponding section
        timelineSections.forEach(section => {
            section.classList.remove('active');
            section.querySelectorAll('.timeline-item').forEach(item => item.classList.remove('visible'));

            if (section.id === `${target}-timeline`) {
                section.classList.add('active');

                // Animate items in with stagger
                const items = section.querySelectorAll('.timeline-item');
                items.forEach((item, index) => {
                    const t = setTimeout(() => item.classList.add('visible'), index * 200);
                    timeouts.push(t);
                });
            }
        });
    });
});

// Skill Progress Bars Animation
const progressBars = document.querySelectorAll('.progress');

function animateProgressBars() {
    progressBars.forEach(progress => {
        const width = progress.getAttribute('data-width');
        progress.style.width = width;
    });
}

// Animate progress bars when in view
const skillsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateProgressBars();
            skillsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

skillsObserver.observe(document.getElementById('skills'));

// Scroll Animation for Elements
const animatedElements = document.querySelectorAll('.bio-card, .skill-item, .certificate-card, .project-card');

const elementsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            elementsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

animatedElements.forEach(element => {
    elementsObserver.observe(element);
});

// Slider for multiple images per project
const sliders = document.querySelectorAll('.project-img-slider');

sliders.forEach(slider => {
    const images = slider.querySelectorAll('img');
    let currentIndex = 0;

    images[currentIndex].classList.add('active');

    const nextBtn = slider.querySelector('.next');
    const prevBtn = slider.querySelector('.prev');

    nextBtn.addEventListener('click', () => {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
    });

    prevBtn.addEventListener('click', () => {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        images[currentIndex].classList.add('active');
    });
});

// Mobile Navigation
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Form Submission
const contactForm = document.getElementById('contactForm');

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Simulate form submission
    const submitBtn = contactForm.querySelector('.submit-btn');
    submitBtn.textContent = 'Sending...';

    setTimeout(() => {
        submitBtn.textContent = 'Message Sent!';
        submitBtn.style.background = 'linear-gradient(90deg, #00cc00, #00ff00)';
        contactForm.reset();

        setTimeout(() => {
            submitBtn.textContent = 'Send Message';
            submitBtn.style.background = 'linear-gradient(90deg, var(--neon-purple), var(--neon-pink))';
        }, 3000);
    }, 1500);
});




// Contact form submission handling
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = form.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    // Show loading state
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    // Submit form via AJAX
    fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            alert('Message sent successfully!');
            form.reset();
        } else {
            // Show error message
            alert('There was an error sending your message. Please try again.');
        }
    })
    .catch(error => {
        alert('There was an error sending your message. Please try again.');
    })
    .finally(() => {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
});



// JavaScript for modal functionality with zoom
document.addEventListener('DOMContentLoaded', function() {
    // Get the modal
    const modal = document.getElementById('certificateModal');
    const modalImg = document.getElementById('modalImg');
    const closeBtn = document.querySelector('.close');
    
    // Zoom variables
    let currentScale = 1;
    const ZOOM_SENSITIVITY = 0.1;
    const MIN_ZOOM = 0.5;
    const MAX_ZOOM = 5;
    
    // Get all view buttons
    const viewButtons = document.querySelectorAll('.view-btn');
    
    // Add click event to all view buttons
    viewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent event from bubbling to parent elements
            const imgSrc = this.getAttribute('data-img');
            modalImg.src = imgSrc;
            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
            
            // Reset zoom when opening a new image
            resetZoom();
        });
    });
    
    // Close modal when clicking on close button
    closeBtn.addEventListener('click', function() {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    });
    
    // Close modal when clicking outside of the image
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
    
    // Zoom functionality
    function zoomImage(scaleFactor) {
        currentScale *= scaleFactor;
        
        // Apply limits
        if (currentScale < MIN_ZOOM) currentScale = MIN_ZOOM;
        if (currentScale > MAX_ZOOM) currentScale = MAX_ZOOM;
        
        // Apply the transformation
        modalImg.style.transform = `scale(${currentScale})`;
    }
    
    function resetZoom() {
        currentScale = 1;
        modalImg.style.transform = 'scale(1)';
        modalImg.style.transformOrigin = 'center center';
    }
    
    // Mouse wheel zoom
    modalImg.addEventListener('wheel', function(e) {
        e.preventDefault();
        if (e.deltaY < 0) {
            // Zoom in
            zoomImage(1 + ZOOM_SENSITIVITY);
        } else {
            // Zoom out
            zoomImage(1 - ZOOM_SENSITIVITY);
        }
    });
    
    // Touch pinch zoom (for mobile devices)
    let initialDistance = null;
    
    modalImg.addEventListener('touchstart', function(e) {
        if (e.touches.length === 2) {
            e.preventDefault();
            initialDistance = Math.hypot(
                e.touches[0].clientX - e.touches[1].clientX,
                e.touches[0].clientY - e.touches[1].clientY
            );
        }
    });
    
    modalImg.addEventListener('touchmove', function(e) {
        if (e.touches.length === 2) {
            e.preventDefault();
            const currentDistance = Math.hypot(
                e.touches[0].clientX - e.touches[1].clientX,
                e.touches[0].clientY - e.touches[1].clientY
            );
            
            if (initialDistance) {
                const scaleFactor = currentDistance / initialDistance;
                currentScale = scaleFactor;
                
                // Apply limits
                if (currentScale < MIN_ZOOM) currentScale = MIN_ZOOM;
                if (currentScale > MAX_ZOOM) currentScale = MAX_ZOOM;
                
                modalImg.style.transform = `scale(${currentScale})`;
            }
        }
    });
    
    modalImg.addEventListener('touchend', function() {
        initialDistance = null;
    });
    
    // Optional: Add zoom buttons to the UI
    const zoomInBtn = document.createElement('button');
    zoomInBtn.className = 'zoom-btn zoom-in';
    zoomInBtn.innerHTML = '+';
    zoomInBtn.addEventListener('click', () => zoomImage(1 + ZOOM_SENSITIVITY));
    
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.className = 'zoom-btn zoom-out';
    zoomOutBtn.innerHTML = '-';
    zoomOutBtn.addEventListener('click', () => zoomImage(1 - ZOOM_SENSITIVITY));
    
    const resetZoomBtn = document.createElement('button');
    resetZoomBtn.className = 'zoom-btn reset-zoom';
    resetZoomBtn.innerHTML = '↺';
    resetZoomBtn.addEventListener('click', resetZoom);
    
    const zoomControls = document.createElement('div');
    zoomControls.className = 'zoom-controls';
    zoomControls.appendChild(zoomInBtn);
    zoomControls.appendChild(zoomOutBtn);
    zoomControls.appendChild(resetZoomBtn);
    
    modal.querySelector('.modal-content').appendChild(zoomControls);
});