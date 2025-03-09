document.addEventListener("DOMContentLoaded", function () {
    let photos = document.querySelectorAll(".photo");

    photos.forEach(photo => {

        const followCursor = (event) => {
            const rect = photo.getBoundingClientRect();
            const photoWidth = rect.width;
            const photoHeight = rect.height;

            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            const relativeX = mouseX / photoWidth - 0.5;
            const relativeY = mouseY / photoHeight - 0.5;

            const rotateY = Math.round(relativeX * 20);
            const rotateX = Math.round(-relativeY * 20);

            photo.style.transform =
                `perspective(1000px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                scale(1.05)
                `;
        };

        const resetTransform = () => {
            photo.style.transform =
                "perspective(1000px)\
            rotateX(0deg)\
            rotateY(0deg)";
        };

        photo.addEventListener("mousemove", followCursor, false);
        photo.addEventListener("mouseleave", resetTransform, false);
    });
});
