// import "../styles/style.css";
import Alpine from "alpinejs";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

window.Alpine = Alpine;

// GSAP scrollToSection function for smooth scrolling
function scrollToSection(selector) {
  // Normalize selector (add . if no prefix)
  const normalizedSelector =
    selector.startsWith(".") || selector.startsWith("#")
      ? selector
      : `.${selector}`;

  const target = document.querySelector(normalizedSelector);
  if (!target) return;

  // Animate scroll using GSAP proxy
  const scrollProxy = {
    scroll: window.pageYOffset || document.documentElement.scrollTop,
  };

  gsap.to(scrollProxy, {
    scroll: target.offsetTop,
    duration: 1.2,
    ease: "power2.inOut",
    onUpdate: () => {
      window.scrollTo(0, scrollProxy.scroll);
      document.documentElement.scrollTop = scrollProxy.scroll;
    },
  });
}

// Make it available globally for Alpine
window.scrollToSection = scrollToSection;

Alpine.start();

// $(document).ready(function() {
//   $('.slider').slick({
//     dots: false,
//     infinite: true,
//     centerMode: true,
//     autoplay: true,
//     autoplaySpeed: 2000,
//     speed: 1000,
//     slidesToShow: 5,
//     pauseOnHover: true,
//     pauseOnFocus: true,
//     cssEase: 'linear',
//     responsive: [
//       {
//         breakpoint: 768,
//         settings: {
//           slidesToShow: 1,
//           centerMode: true,
//           centerPadding: '80px',
//           autoplaySpeed: 2000,
//           speed: 1000,
//         }
//       }
//     ]
//   });
// });

// Initialize read more functionality for elements with .read-more class
function initReadMore() {
  const readMoreElements = document.querySelectorAll(".read-more");

  readMoreElements.forEach((container) => {
    const paragraph = container.querySelector("p");
    if (!paragraph) return;

    // Temporarily add line-clamp to check if truncation is needed
    paragraph.classList.add("line-clamp-4");
    const needsTruncation = paragraph.scrollHeight > paragraph.clientHeight;
    paragraph.classList.remove("line-clamp-4");

    // Only add functionality if content exceeds 4 lines
    if (!needsTruncation) return;

    // Add line-clamp class
    paragraph.classList.add("line-clamp-4");

    // Create read more button
    const button = document.createElement("button");
    button.className =
      "text-emerald font-medium font-sans hover:text-lemon transition-colors duration-300 mt-2";
    button.textContent = "Read more";

    button.addEventListener("click", () => {
      paragraph.classList.remove("line-clamp-4");
      paragraph.classList.add("line-clamp-none");
      button.remove(); // Remove button after expanding
    });

    container.appendChild(button);
  });
}

// document.addEventListener("DOMContentLoaded", () => {
const fadeInUpElements = gsap.utils.toArray(".fadeInUp");

fadeInUpElements.forEach((element) => {
  // console.log("fadeInUpElements", element);
  gsap.from(element, {
    opacity: 0,
    y: 40,
    duration: 0.8,
    ease: "power2.out",
    scrollTrigger: {
      trigger: element,
      start: "top 85%",
      toggleActions: "play none none reverse",
    },
  });
});

const spinElements = gsap.utils.toArray(".spin");

spinElements.forEach((element) => {
  gsap.fromTo(
    element,
    { rotate: 0 },
    {
      rotate: 360,
      duration: 1.1,
      ease: "power2.out",
      scrollTrigger: {
        trigger: element,
        start: "top 85%",
        toggleActions: "restart none none reverse",
      },
    },
  );
});

// Initialize read more functionality
initReadMore();
// });
