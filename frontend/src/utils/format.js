/** ISO 문자열을 게시판 목록용 MM.DD 로 줄인다. */
export function formatShortDate(iso) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${mm}.${dd}`
}

/** 상세 화면용 YYYY.MM.DD HH:mm */
export function formatFullDate(iso) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(
    d.getMinutes(),
  )}`
}

/** 주소에서 '서울특별시' 접두사를 떼고 구·동까지만 남긴다. */
export function shortAddress(address) {
  if (!address) return ''
  return address.replace(/^서울특별시\s*/, '').split(' ').slice(0, 2).join(' ')
}
