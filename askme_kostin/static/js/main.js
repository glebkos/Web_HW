function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items = document.getElementsByClassName('like-section');

for (let item of items) {
    const [like, counter, dislike] = item.children
    like.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('question_id', like.dataset.id)

        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
                if (data.activate) {
                    like.classList.remove("btn-outline-success");
                    dislike.classList.remove("btn-danger");
                    dislike.classList.add("btn-outline-danger");
                    like.classList.add("btn-success");
                } else {
                    like.classList.remove("btn-success");
                    like.classList.add("btn-outline-success");
                }
            });
    })

    dislike.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('question_id', dislike.dataset.id)

        const request = new Request('/dislike/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
                if (data.activate) {
                    dislike.classList.remove("btn-outline-danger");
                    like.classList.remove("btn-success");
                    like.classList.add("btn-outline-success");
                    dislike.classList.add("btn-danger");
                } else {
                    dislike.classList.remove("btn-danger");
                    dislike.classList.add("btn-outline-danger");
                }
            });
    })
}

const correctAnswers = document.getElementsByClassName('correct-section');

for (let item of correctAnswers) {
    const [correct, ] = item.children
    correct.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('question_id', correct.dataset.qid)
        formData.append('answer_id', correct.dataset.aid)

        const request = new Request('/correct/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
    })
}