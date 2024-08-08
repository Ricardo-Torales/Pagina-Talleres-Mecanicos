document.addEventListener('DOMContentLoaded', () => {
    const follower = document.getElementById('follower');

    document.addEventListener('mousemove', (e) => {
        if (follower.style.display === 'block') {
            const x = e.pageX - follower.offsetWidth;
            const y = e.pageY - follower.offsetHeight;
            follower.style.transform = `translate(${x}px, ${y}px) scale(1)`;
        }
    });

    document.addEventListener('mouseenter', () => {
        follower.style.display = 'block';
    });

    document.addEventListener('mouseleave', () => {
        follower.style.display = 'none';
        follower.style.transform = 'scale(0)'; /* Restauramos la escala cero para ocultar completamente */
    });
});
