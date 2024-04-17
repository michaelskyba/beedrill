<script>
	let username;
	let password;

	async function submit() {
		const response = await fetch("http://127.0.0.1:8000/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		});

		const data = await response.json();
		alert("Done")
		console.log(data)
	}
</script>

<label for="username">Username</label>
<input id="username" bind:value={username}>

<label for="password">Password</label>
<input id="password" type="password" bind:value={password}>

<br>

<button on:click={submit}>Submit</button>
