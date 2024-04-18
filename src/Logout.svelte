<script>
	import { user, page } from "./store.js";

	const logout = () => {
		user.set(null);
		page.set("home");
	}
</script>

<button on:click={logout}>Log out</button>
