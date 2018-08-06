const follow = async (event, to_profile, username) => {
  event.preventDefault()
  let csrfmiddlewaretoken = document.getElementById(`form-follow-${to_profile}`).elements.namedItem("csrfmiddlewaretoken").value
  let data = new FormData()
  data.append('csrfmiddlewaretoken', csrfmiddlewaretoken)
  data.append('to_profile', to_profile)
  let response = await fetch(`/users/${username}/follow`, {
    method: 'POST',
    body: data,
    credentials: 'same-origin',
  })
  let { status, message } = await response.json()

  let text = document.getElementById('textToChange')
  text.innerHTML = message
  //console.log(text)
  console.log(status, '', message)
}