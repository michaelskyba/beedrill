<script>
	export let pageLinked;
	export let text;
	export let disabled = false;

	import { page } from "./store.js";

	const click = () => {
		page.set(pageLinked);
	}

	let buttonClass;
	page.subscribe(v => {
		if (v == pageLinked || (v == "edit_deck" && pageLinked == "my_decks"))
			buttonClass = "active";
		else
			buttonClass = "inactive";
	})
</script>

{#if disabled}
	<button class={buttonClass} disabled>{text}</button>
{:else}
	<button class={buttonClass} on:click={click}>{text}</button>
{/if}

<style>
	button.active {
		background-color: #005C46;
		border-color: #005C46;
		color: #ffffff;
		outline: 0;
	}
</style>
