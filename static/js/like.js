const like = async (event, post) => {
  event.preventDefault()
  let csrfmiddlewaretoken = document.getElementById(`form-like-${post}`).elements.namedItem("csrfmiddlewaretoken").value
  let data = new FormData()
  data.append('csrfmiddlewaretoken', csrfmiddlewaretoken)
  data.append('post', post)

  let response = await fetch(`/posts/${post}/like`, {
    method: 'POST',
    body: data,
    credentials: 'same-origin',
  })
  let { status } = await response.json()
  if (status == true){
    event.target.parentElement.style.color = 'red'
    let text = event.target.parentElement.nextElementSibling
    text.innerHTML = parseInt(text.innerHTML)+1
  } else {
    event.target.parentElement.style.color = 'black'
    let text = event.target.parentElement.nextElementSibling
    text.innerHTML = parseInt(text.innerHTML)-1
  }
}