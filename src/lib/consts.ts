import { isHttpError } from '@sveltejs/kit';
import { toast } from 'svelte-sonner';

export function handleError(err: unknown) {
	if (isHttpError(err)) {
		toast.error(err.body.message);
	} else {
		toast.error('Unhandled error');
	}
}
