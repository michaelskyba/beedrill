<script>
	import { reviewState } from "./store.js";
</script>

<blockquote>
	<h3>Front</h3>
	<hr>
	{#if $reviewState.step == "front"}
		<h3>...</h3>
	{:else}
		<h3>Back</h3>
	{/if}
</blockquote>

<hr>

{#if $reviewState.step == "front"}
	<div id="review">
		<button>Show back</button>
	</div>
{:else}
	<p>Did you correctly recall this card?</p>

	<div id="review">
		<button>Correct</button>
		<button>Incorrect</button>
	</div>
{/if}

<style>
	h3, p {
		text-align: center;
	}

	blockquote {
		padding: 2em;
	}

	hr {
		margin: 2em;
	}

	div#review {
		display: flex;
		justify-content: center;
		align-content: center;
		gap: 1em;
	}
</style>
