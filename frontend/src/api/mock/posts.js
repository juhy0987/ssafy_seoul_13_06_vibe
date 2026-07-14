/**
 * 백엔드(FastAPI + SQLite)가 붙기 전까지 화면 확인용으로 쓰는 시드 게시글.
 * 백엔드 완성 후에는 이 파일이 초기 DB 시드의 원본이 된다.
 */
export const MOCK_POSTS = [
  {
    id: 7,
    category: 'attraction',
    title: '경복궁 야간개장 다녀왔어요',
    content:
      '지난 주말 경복궁 야간개장에 다녀왔습니다. 근정전 조명이 특히 인상적이었어요.\n예매는 정확히 오픈 시각에 들어가야 자리가 남습니다. 광화문역 2번 출구에서 걸어서 5분이면 도착해요.',
    view_count: 128,
    created_at: '2026-07-14T20:10:00',
  },
  {
    id: 6,
    category: 'attraction',
    title: '북촌 한옥마을 사진 명소 정리',
    content:
      '북촌 8경 중에서 사람이 덜 몰리는 곳 위주로 정리해봤습니다.\n주민이 실제로 거주하는 골목이니 조용히 다녀오시길 부탁드려요.',
    view_count: 94,
    created_at: '2026-07-13T15:42:00',
  },
  {
    id: 5,
    category: 'festival',
    title: '여의도 밤도깨비 야시장 이번 주 열려요',
    content:
      '이번 주 금·토 저녁에 여의도 한강공원에서 밤도깨비 야시장이 열립니다.\n푸드트럭 줄이 길어서 6시 전에 도착하는 걸 추천드려요.',
    view_count: 211,
    created_at: '2026-07-12T18:05:00',
  },
  {
    id: 4,
    category: 'culture',
    title: 'DDP 전시 후기 (디자인 아카이브)',
    content: '동대문디자인플라자 전시 다녀왔습니다. 평일 오전이 한산해서 관람하기 좋았어요.',
    view_count: 63,
    created_at: '2026-07-11T11:20:00',
  },
  {
    id: 3,
    category: 'attraction',
    title: '남산타워 야경 포인트 추천',
    content: '케이블카보다 남산 순환버스가 훨씬 빨랐습니다. 해 지기 30분 전 도착이 베스트예요.',
    view_count: 152,
    created_at: '2026-07-10T21:30:00',
  },
  {
    id: 2,
    category: 'culture',
    title: '서울공예박물관 무료 관람 팁',
    content: '안국역 근처 서울공예박물관은 상설 전시가 무료입니다. 도슨트 시간 맞춰 가면 좋아요.',
    view_count: 47,
    created_at: '2026-07-09T14:00:00',
  },
  {
    id: 1,
    category: 'festival',
    title: '한강 불꽃축제 올해 일정 아시는 분',
    content: '매년 10월 초에 열렸는데 올해 공식 일정 나왔는지 궁금합니다.',
    view_count: 305,
    created_at: '2026-07-08T09:15:00',
  },
]
