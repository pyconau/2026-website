import { gsap } from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"
import Alpine from 'alpinejs'

gsap.registerPlugin(ScrollTrigger)
window.gsap = gsap

window.Alpine = Alpine
Alpine.start()

// Check if this is a first-time visitor
const hasVisitedBefore = sessionStorage.getItem('pycon-visited');

if (!hasVisitedBefore) {
  // Only initialize animation for first-time visitors and on larger screens
  const curlyboiiElement = document.getElementById('curlyboii');
  
  if (curlyboiiElement && window.innerWidth >= 1024) { // lg breakpoint
    const animation = lottie.loadAnimation({
      container: curlyboiiElement,
      renderer: "svg",
      loop: false,
      autoplay: true,
      path: "./CurlyBoi_Animated.json",
      rendererSettings: {
          id: "curlyboii",
      },
    });

    animation.addEventListener('enterFrame', () => {
      const progress = animation.currentFrame / animation.totalFrames;
      if (progress >= 0.4 && !window.loadScreenStarted) {
          window.loadScreenStarted = true;
          initLoadScreen();
      }
    });

    // Dispatch event when animation completes
    animation.addEventListener('complete', () => {
      window.dispatchEvent(new CustomEvent('animation-complete'));
    });
  } else {
    // On mobile or if element doesn't exist, skip straight to load screen
    initLoadScreen();
  }
} else {
  // For returning visitors, skip directly to the final state
  initLoadScreen();
}

// Load screen animation
function initLoadScreen() {
  // Create timeline for load screen
  const loadTimeline = gsap.timeline()  
  
  // Set initial states
  // gsap.set("#curlyboi", { y: 0 })
  // gsap.set("#pycon26", { width: "333px" })
  // gsap.set(".time-date", { fontSize: "70px" })

  gsap.set(".bg-separator", { y: "100%" })
  
  // Animate load screen
  loadTimeline
    // .to("#curlyboi", {
    //   y: "-120%",
    //   duration: 2,
    //   ease: "power2.inOut"
    // })    
    .to("#pycon26", {
      opacity: 1,
      y: 0,
      duration: 2,
      ease: "power2.out"
    }, "0")
    .to(".time-date", {
      opacity: 1,
      y: 0,
      fontSize: "2.25rem", // text-4xl equivalent
      duration: 1.2,
      ease: "power2.out"
    }, "-=1.0")
    .to(".bg-separator", {
      y: 0,
      duration: 1.5,
      ease: "power2.out"
    }, "-=1.0")
}

// Initialize load screen when page loads
// window.addEventListener('load', initLoadScreen)

// Pin first section and wipe over effect
gsap.timeline({
  scrollTrigger: {
    trigger: "#hero-section",
    start: "top top",
    end: "+=100%",
    pin: true,
    pinSpacing: false,
    scrub: 1
  }
})

gsap.utils.toArray('.fade-up').forEach((element) => {
  gsap.fromTo(element, 
    {
      y: 50,
      opacity: 0
    },
    {
      y: 0,
      opacity: 1,
      duration: 0.8,
      ease: "power2.out",
      scrollTrigger: {
        trigger: element,
        start: "top 80%",
        end: "bottom 20%",
        toggleActions: "play none none reverse"
      }
    }
  )
})

gsap.utils.toArray('.fade-up-stagger').forEach((group) => {
  const children = group.querySelectorAll('.fade-up-item')
  
  gsap.fromTo(children,
    {
      y: 50,
      opacity: 0
    },
    {
      y: 0,
      opacity: 1,
      duration: 0.8,
      ease: "power2.out",
      stagger: 0.2,
      scrollTrigger: {
        trigger: group,
        start: "top 80%",
        end: "bottom 20%",
        toggleActions: "play none none reverse"
      }
    }
  )
})

// Slide up only (no fade)
gsap.utils.toArray('.slide-up').forEach((element) => {
  gsap.fromTo(element, 
    {
      y: 20
    },
    {
      y: 0,
      duration: 0.8,
      ease: "power2.out",
      scrollTrigger: {
        trigger: element,
        start: "top 80%",
        end: "bottom 20%",
        toggleActions: "play none none reverse"
      }
    }
  )
})

gsap.utils.toArray('.slide-up-stagger').forEach((group) => {
  const children = group.querySelectorAll('.slide-up-item')
  
  gsap.fromTo(children,
    {
      y: 20
    },
    {
      y: 0,
      duration: 0.8,
      ease: "power2.out",
      stagger: 0.2,
      scrollTrigger: {
        trigger: group,
        start: "top 80%",
        end: "bottom 20%",
        toggleActions: "play none none reverse"
      }
    }
  )
})