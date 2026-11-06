// Reader navigation stays on this site. Public source URIs may be retained
// as citation text; they are not navigation destinations.
export function isReaderHref(href) {
  return typeof href === 'string' && !/[\\\u0000-\u0020\u007f]/.test(href) &&
    ((href.startsWith('/') && !href.startsWith('//')) || (href.startsWith('#') && href.length > 1));
}
