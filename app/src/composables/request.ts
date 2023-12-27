export const useRequest = <Req, Res>() => {
  const request = async (
    url: string,
    body?: Req,
    options?: RequestInit,
    refetch?: boolean,
  ) => {
    const requestOptions: RequestInit = {
      ...options,
      ...(body && { body: JSON.stringify(body) }),
    };
    const {
      data,
      error,
      isFetching: loading,
    } = await useFetch(url, requestOptions, {
      refetch: refetch || false,
    }).json<Res>();
    return { data, error, loading };
  };
  return request;
};
