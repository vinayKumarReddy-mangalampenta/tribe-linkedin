function deleteMessage(elem) {
    elem.parentElement.remove()
    setMessages()
}

const setMessages = () => {
    let messages = document.getElementsByClassName('alert')

    for (let i = 0; i < messages.length; i++) {
        const elem = messages[i]
        elem.style.top = `${80 * i}px`;
    }
}

setMessages()












const is_authenticated = document.getElementById('user-authenticated')
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


let colors = {
    like: 'yellow',
    love: 'red',
    cheers: '#960c91',
    claps: 'green',
    laugh: "#898e2e",
    hundred: '#1be51b;'
}

function likePost(elem) {
    console.log(elem.dataset)
    value = elem.dataset.value
    post = elem.dataset.post
    let cookies = document.cookie
    console.log(is_authenticated.value)
    if (is_authenticated.value === 'True') {
        fetch('http://127.0.0.1:8000/api/like-post/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ value, post })
        })
            .then((response) => (
                response.json()
            ))
            .then((data) => {
                elem.parentElement.parentElement.lastElementChild.innerHTML = value
                elem.parentElement.parentElement.lastElementChild.className = `btn--like value--${value}`

                if (data['likesCount'] === 1) {
                    elem.parentElement.parentElement.parentElement.parentElement.children[2].children[0].innerHTML = '1 Like'
                } else {
                    elem.parentElement.parentElement.parentElement.parentElement.children[2].children[0].innerHTML = `${data.likesCount} Likes`
                }
            })
    } else {
        window.location.href = `/members/login/?next=#${post}`
    }

}

function likeOrRemoveLike(elem) {
    let post = elem.dataset.post
    let cookies = document.cookie
    if (is_authenticated.value === 'True') {
        fetch('http://127.0.0.1:8000/api/toggle-like-post/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ post })
        })
            .then((response) => (
                response.json()
            ))
            .then((data) => {
                if (data['status'] === 'like deleted') {
                    elem.innerHTML = `   <span class="interaction-btn-logo">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke="white" aria-hidden="true"
                            class="h-5 w-5 -ml-1 mr-2 w-6 h-6 transition-transform group-hover:-rotate-6"
                            focusable="false">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5">
                            </path>
                        </svg>
                    </span>
                    <span style='color:white;'>
                        Like
                    </span>`

                    elem.className = `btn--like`
                } else {
                    elem.innerHTML = `  
                    <span style='color:yellow;'>
                        Like
                    </span>`

                    elem.className = `btn--like value--like`
                }


                if (data['likesCount'] === 1) {
                    elem.parentElement.parentElement.parentElement.children[2].children[0].innerHTML = '1 Like'
                } else {
                    elem.parentElement.parentElement.parentElement.children[2].children[0].innerHTML = `${data.likesCount} Likes`
                }

            })
    } else {
        window.location.href = `/members/login/?next=#${post}`
    }

}
