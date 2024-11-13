// const fadeout=() => {
//     const loader = document.querySelector("#preloader");
//     loader.style.display = "none";
// }

// window.addEventListener("load",fadeout);
// document.addEventListener("DOMContentLoaded", function() {
//     const fadeout = () => {
//         const loader = document.getElementById("preloader");

//         if (loader) {
//             setTimeout(() => {
//                 loader.style.display = "none";
//             }, 3000);
//         } else {
//             console.log("");
//         }
//     }
//     window.addEventListener("load", fadeout);
// });
// Define the fadeout function
const fadeout = () => {
    const loader = document.getElementById("preloader");
    if (loader) {
        setTimeout(() => {
            loader.style.display = "none";
        }, 1000); // 3 seconds delay
    }
};

// Ensure the fadeout function is called once the window has fully loaded
window.addEventListener("load", fadeout);