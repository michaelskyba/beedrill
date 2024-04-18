<script>
	import { user } from "./store.js";
</script>

<p>
	Welcome to Beedrill.

	{#if $user}
		You are logged in as <code>{$user.username}</code>.
	{:else}
		You are logged out.
	{/if}
</p>

