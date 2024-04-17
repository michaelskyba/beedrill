<script>
	let username;
	let password;

	const submit = () => {
		alert(`Submitting ${username} ${password}`);
	}
</script>

<label for="username">Username</label>
<input id="username" bind:value={username}>

<label for="password">Password</label>
<input id="password" type="password" bind:value={password}>

<br>

<button on:click={submit}>Submit</button>
