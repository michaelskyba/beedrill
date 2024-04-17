<script>
	export let pageLinked;
	export let text;

	import { page } from "./store.js";

	const click = () => {
		page.set(pageLinked);
	}
</script>

{#if $page == pageLinked}
	<button class="active" on:click={click}>{text}</button>
{:else}
	<button on:click={click}>{text}</button>
{/if}

<style>
	button.active {
		background-color: white;
		color: black;
	}
</style>
