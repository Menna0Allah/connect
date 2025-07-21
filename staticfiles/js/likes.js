// Added: JavaScript for handling like/unlike actions via AJAX
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const type = this.getAttribute('data-type');
            const id = this.getAttribute('data-id');
            const url = type === 'room' ? `/like-room/${id}` : `/like-message/${id}`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                const heartIcon = this.querySelector('i');
                const countSpan = this.querySelector('.like-count');
                
                if (data.liked) {
                    this.classList.add('liked');
                    heartIcon.classList.replace('bi-heart', 'bi-heart-fill');
                    this.title = 'Unlike';
                } else {
                    this.classList.remove('liked');
                    heartIcon.classList.replace('bi-heart-fill', 'bi-heart');
                    this.title = 'Like';
                }
                countSpan.textContent = data.like_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = cookie.substring(name.length + 1);
                    break;
                }
            }
        }
        return cookieValue;
    }
});