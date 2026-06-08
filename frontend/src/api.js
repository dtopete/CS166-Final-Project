const jsonHeaders = { 'Content-Type': 'application/json' }

export async function fetchAll(path) {
  try {
    const response = await fetch(path)
    if (!response.ok) {
      return []
    }
    return await response.json()
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function postResource(path, payload) {
  try {
    const response = await fetch(path, {
      method: 'POST',
      headers: jsonHeaders,
      body: JSON.stringify(payload)
    })
    return await response.json()
  } catch (error) {
    console.error(error)
    return { error: 'Unable to reach backend' }
  }
}

export async function patchResource(path, payload) {
  try {
    const response = await fetch(path, {
      method: 'PATCH',
      headers: jsonHeaders,
      body: JSON.stringify(payload)
    })
    return await response.json()
  } catch (error) {
    console.error(error)
    return { error: 'Unable to reach backend' }
  }
}
