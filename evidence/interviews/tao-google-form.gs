// Tạo Google Form phỏng vấn (bản tự điền, có rẽ nhánh, toàn câu chọn) + Google Sheet nhận câu trả lời.
// Cách chạy: script.google.com → dán file này → Run "taoForm" → cấp quyền → xem link trong Nhật ký thực thi.
// Rẽ nhánh theo mức quen trang pre-class:
//   Đã dùng → [A] xem video pre-class → (đã hỏi trợ giảng AI? → [A2] : [B2]) → [E]
//   Biết nhưng chưa dùng → [C] vì sao chưa dùng → [D] học qua video nói chung → [E]
//   Không biết trang → [D] → [E]
// Hỏi theo kiểu "lần gần nhất" (GUIDE.md), không giới thiệu ý tưởng của nhóm, không thu tên/email/mã học viên.
// Câu nào có "Mục khác" thì người trả lời tự gõ được → đó là nguồn trích dẫn nguyên văn.

function taoForm() {
  var form = FormApp.create('Bạn học qua video bài giảng thế nào? (3–5 phút, toàn bấm chọn)');
  form.setDescription(
    'Nhóm Siuu (khoá AI20K) đang tìm hiểu cách mọi người tự học qua video bài giảng. ' +
    'Không giới thiệu sản phẩm gì cả, không có đáp án đúng/sai. ' +
    'Không cần ghi tên, email hay mã học viên.\n\n' +
    'Mẹo: hãy chọn theo LẦN GẦN NHẤT thật sự xảy ra, không phải "thường thì". ' +
    'Không có lựa chọn đúng ý thì gõ vào ô "Khác" — nhóm rất thích đọc ô này.');
  form.setCollectEmail(false);

  // Câu chọn 1 / chọn nhiều — viết gọn
  function mot(title, choices, other) {
    var q = form.addMultipleChoiceItem().setTitle(title).setChoiceValues(choices);
    if (other) q.showOtherOption(true);
    return q;
  }
  function nhieu(title, choices, other) {
    var q = form.addCheckboxItem().setTitle(title + ' (chọn nhiều)').setChoiceValues(choices);
    if (other) q.showOtherOption(true);
    return q;
  }

  // ── Phần 1: bạn là ai ──
  mot('Bạn là', ['Học viên khoá AI20K (L3A / L3B)', 'Đang học một khoá online khác về AI / IT',
    'Sinh viên', 'Người đi làm tự học thêm'], true).setRequired(true);
  var qBiet = form.addMultipleChoiceItem().setRequired(true)
    .setTitle('Khoá AI20K có "trang pre-class": trang để xem video bài giảng trước buổi học, ' +
      'dưới video có ô hỏi trợ giảng AI. Bạn đã dùng trang này chưa?');

  // ── [A] Đã dùng trang pre-class ──
  var pA = form.addPageBreakItem().setTitle('Lần gần nhất bạn xem video trên trang pre-class');
  mot('A1. Lần gần nhất là khi nào?',
    ['Hôm nay', 'Hôm qua', 'Mấy hôm trước, trong tuần này', 'Tuần trước', 'Lâu hơn nữa', 'Không nhớ']).setRequired(true);
  mot('A2. Lúc mấy giờ?',
    ['Sáng sớm trước khi đi làm / đi học (5h–9h)', 'Trong giờ hành chính, xem "lén" 🤫 (9h–17h)',
      'Chiều tối (17h–21h)', 'Đêm khuya (21h–1h)', 'Sau 1h sáng — cú đêm chính hiệu 🦉', 'Không nhớ']);
  nhieu('A3. Xem ở đâu, bằng gì?',
    ['Ở nhà, trên laptop', 'Trên điện thoại', 'Trên xe bus / Grab', 'Ở công ty',
      'Quán cà phê', 'Trên giường, nửa thức nửa ngủ 😴'], true);
  mot('A4. Lần đó có đoạn nào bạn chưa hiểu hoặc phải xem lại không?',
    ['Có, 1 đoạn', 'Có, vài đoạn', 'Có, gần như cả video 😵', 'Không, hiểu hết',
      'Không để ý, vì vừa xem vừa làm việc khác']).setRequired(true);
  nhieu('A5. Lần đó bạn đã thử những cách nào?',
    ['Tua lại để tìm đoạn đó', 'Xem lại từ đầu video', 'Chỉnh tốc độ chậm lại rồi nghe lại',
      'Hỏi trợ giảng AI dưới video', 'Đọc lại slide / tài liệu', 'Hỏi bạn / giảng viên / trợ giảng người',
      'Hỏi ChatGPT / Gemini / AI khác', 'Ghi chú lại để hỏi trên lớp', 'Ngồi nhìn màn hình suy nghĩ 🤔',
      'Bỏ qua, xem tiếp'], true);
  nhieu('A6. Cách đó vướng ở đâu?',
    ['Tua mãi không tìm đúng đoạn', 'Thanh tua quá nhạy, tua lố cả 2 phút', 'Xem lại vẫn không hiểu vì giảng y như cũ',
      'Câu trả lời của AI chung chung, không gắn với bài', 'Không biết hỏi sao cho đúng',
      'Mất thời gian quá nên bỏ', 'Không vướng gì, ổn'], true);
  nhieu('A7. Vì sao bạn vẫn dùng cách đó?',
    ['Nhanh nhất mình biết', 'Quen tay rồi', 'Lúc đó không có ai để hỏi', 'Không có cách nào khác',
      'Có sẵn, miễn phí'], true);
  var qDaHoi = form.addMultipleChoiceItem().setRequired(true)
    .setTitle('A8. Bạn đã bao giờ hỏi trợ giảng AI ngay dưới video chưa?');

  // ── [A2] Đã hỏi trợ giảng AI ──
  var pA2 = form.addPageBreakItem().setTitle('Lần gần nhất bạn hỏi trợ giảng AI dưới video');
  nhieu('H1. Lần đó bạn hỏi kiểu gì?',
    ['Hỏi nghĩa một thuật ngữ / khái niệm', 'Nhờ giải thích lại một đoạn vừa giảng', 'Xin ví dụ minh hoạ',
      'Bôi đen chữ trên slide rồi hỏi', 'Hỏi về câu hỏi giữa video', 'Hỏi thứ không có trong bài',
      'Gõ "?" hoặc "cái này là sao" cho nhanh'], true).setRequired(true);
  mot('H2. Câu trả lời có chỉ ra đoạn nào trong video / bài để bạn mở ra xem lại không?',
    ['Có, và mình đã mở lại đúng đoạn đó', 'Có, nhưng mình không mở / mở ra không đúng chỗ',
      'Không chỉ ra đoạn nào', 'Không nhớ']);
  mot('H3. Sau khi đọc câu trả lời, bạn đã hiểu ý đó chưa?',
    ['Hiểu luôn', 'Hiểu một phần, phải tìm thêm', 'Chưa hiểu, phải hỏi lại hoặc hỏi chỗ khác',
      'Tưởng hiểu, lên lớp mới biết là chưa 😅', 'Bỏ qua']);
  mot('H4. Có lần nào trợ giảng trả lời điều bài không dạy, hoặc lạc đề không?',
    ['Có, và mình tin luôn', 'Có, mình nghi nên kiểm lại bài', 'Có, mình bỏ qua câu trả lời đó',
      'Chưa thấy lần nào', 'Không biết — làm sao mà biết được 🤷']);
  nhieu('H5. Khi muốn kiểm lại câu trả lời, bạn làm gì?',
    ['Tua lại video tìm đoạn đó', 'Hỏi lại lần nữa xem có trả lời khác không', 'Hỏi ChatGPT để "đối chứng"',
      'Hỏi bạn', 'Không kiểm, tin luôn'], true);

  // ── [B2] Đã dùng trang nhưng chưa hỏi trợ giảng AI ──
  var pB2 = form.addPageBreakItem().setTitle('Bạn chưa hỏi trợ giảng AI dưới video');
  nhieu('K1. Vì sao bạn chưa hỏi?',
    ['Không để ý là có ô hỏi', 'Chưa gặp chỗ nào cần hỏi', 'Hỏi ChatGPT / AI khác quen hơn',
      'Không tin câu trả lời sẽ đúng với bài', 'Ngại gõ câu hỏi, tua lại nhanh hơn', 'Không biết hỏi gì',
      'Sợ hỏi câu ngớ ngẩn (dù biết là AI 🙈)'], true);
  nhieu('K2. Lần gần nhất chưa hiểu một đoạn video pre-class, cuối cùng bạn hiểu ra nhờ đâu?',
    ['Tua lại xem', 'Hỏi ChatGPT / AI khác', 'Hỏi bạn', 'Lên lớp nghe giảng', 'Tự đọc tài liệu',
      'Đến giờ vẫn chưa hiểu 🫠'], true);

  // ── [C] Biết trang nhưng chưa dùng ──
  var pC = form.addPageBreakItem().setTitle('Bạn biết trang pre-class nhưng chưa dùng');
  nhieu('C1. Vì sao bạn chưa dùng?',
    ['Không có thời gian trước buổi học', 'Học trên LMS / YouTube / tài liệu khác rồi', 'Không biết vào trang ở đâu',
      'Thấy không cần, lên lớp nghe là đủ', 'Quên mất là có trang này', 'Định dùng mãi mà chưa dùng 😬'], true);
  nhieu('C2. Trước buổi học gần nhất, bạn chuẩn bị bài bằng cách nào?',
    ['Không chuẩn bị, lên lớp tính', 'Đọc slide', 'Xem video trên LMS / YouTube', 'Nhờ bạn tóm tắt',
      'Nhờ ChatGPT tóm tắt bài', 'Lướt qua tiêu đề bài cho có'], true);

  // ── [D] Học qua video bài giảng nói chung (cho người chưa dùng trang) ──
  var pD = form.addPageBreakItem().setTitle('Lần gần nhất bạn tự học qua video bài giảng (khoá online, YouTube, Coursera, Udemy…)');
  mot('D1. Lần gần nhất là khi nào?',
    ['Hôm nay', 'Hôm qua', 'Mấy hôm trước, trong tuần này', 'Tuần trước', 'Lâu hơn nữa', 'Không nhớ']).setRequired(true);
  nhieu('D2. Học trên đâu?',
    ['YouTube', 'Coursera / Udemy / edX', 'LMS của trường / công ty', 'Video lớp quay lại',
      'TikTok / Reels (học thật đấy 😎)'], true);
  nhieu('D3. Chủ đề gì?',
    ['AI / Machine Learning', 'Lập trình', 'Data / phân tích dữ liệu', 'Ngoại ngữ', 'Kỹ năng mềm'], true);
  mot('D4. Lần đó có đoạn nào bạn chưa hiểu hoặc phải xem lại không?',
    ['Có, 1 đoạn', 'Có, vài đoạn', 'Có, gần như cả video 😵', 'Không, hiểu hết',
      'Không để ý, vì vừa xem vừa làm việc khác']).setRequired(true);
  nhieu('D5. Lần đó bạn đã thử những cách nào?',
    ['Tua lại để tìm đoạn đó', 'Xem lại từ đầu video', 'Chỉnh tốc độ chậm lại rồi nghe lại', 'Đọc lại slide / tài liệu',
      'Hỏi bạn / giảng viên / trợ giảng', 'Hỏi ChatGPT / Gemini / AI khác', 'Đọc bình luận dưới video',
      'Tìm video hoặc bài viết khác', 'Bỏ qua, xem tiếp'], true);
  mot('D6. Khi hỏi AI (ChatGPT, Gemini…) về nội dung một bài giảng, câu trả lời thường thế nào?',
    ['Khớp với bài giảng', 'Đúng nhưng giải thích khác cách bài dạy, càng đọc càng rối', 'Có chỗ sai / bịa',
      'Không biết vì không kiểm', 'Chưa từng hỏi AI về bài giảng']);
  nhieu('D7. Khi muốn kiểm lại câu trả lời của AI, bạn làm gì?',
    ['Tua lại video tìm đoạn đó', 'Hỏi lại AI lần nữa', 'Hỏi AI khác để "đối chứng"', 'Google', 'Hỏi bạn',
      'Không kiểm, tin luôn'], true);

  // ── [E] Câu chung cho mọi người ──
  var pE = form.addPageBreakItem().setTitle('Câu cuối — ai cũng trả lời');
  mot('E1. Lần gần nhất chưa hiểu một đoạn video: từ lúc thấy chưa hiểu đến lúc hiểu (hoặc bỏ qua) mất bao lâu?',
    ['Dưới 5 phút', '5–15 phút', '15–30 phút', 'Trên 30 phút', 'Không nhớ', 'Chưa gặp lần nào']);
  mot('E2. Trong 1 tháng qua, việc chưa hiểu một đoạn video bài giảng xảy ra khoảng bao nhiêu lần?',
    ['0 lần', '1–2 lần', '3–5 lần', '6–10 lần', 'Trên 10 lần — gần như bài nào cũng có', 'Không nhớ']);
  nhieu('E3. Khi cần tìm lại một đoạn trong video dài, bạn tìm bằng cách nào?',
    ['Kéo thanh tua dò từng đoạn', 'Bấm lùi 10 giây liên tục', 'Xem lại từ đầu', 'Dùng mục lục / chương của video',
      'Tìm trong phụ đề / transcript', 'Nhớ đại khái phút thứ mấy', 'Nhờ bạn chỉ', 'Thôi khỏi tìm'], true);
  mot('E4. Lần gần nhất tìm lại một đoạn như vậy mất bao lâu?',
    ['Dưới 1 phút', '1–3 phút', '3–5 phút', '5–10 phút', 'Trên 10 phút', 'Bỏ cuộc trước khi tìm thấy 🏳️']);
  nhieu('E5. Video bài giảng gần nhất bạn mở mà không xem hết là vì sao?',
    ['Hết thời gian / có việc gấp', 'Buồn ngủ 😪', 'Video dài quá', 'Không hiểu đoạn giữa nên nản',
      'Đã biết nội dung rồi', 'Xem tiếp ở chỗ khác (LMS, YouTube…)', 'Mạng lag', 'Định xem tiếp mà quên',
      'Không có video nào bỏ dở'], true);
  mot('E6. Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không?',
    ['Có — mình sẽ nhắn lại người đã gửi form này', 'Không, cảm ơn']);

  // Rẽ nhánh — đặt sau khi đã có đủ các phần
  qBiet.setChoices([
    qBiet.createChoice('Đã dùng (dù chỉ vài lần)', pA),
    qBiet.createChoice('Biết trang này nhưng chưa dùng', pC),
    qBiet.createChoice('Chưa nghe đến trang này', pD)
  ]);
  qDaHoi.setChoices([
    qDaHoi.createChoice('Đã hỏi ít nhất 1 lần', pA2),
    qDaHoi.createChoice('Chưa hỏi bao giờ', pB2)
  ]);
  // setGoToPage trên một page break = "hết phần ĐỨNG TRƯỚC nó thì nhảy tới đâu"
  pB2.setGoToPage(pE);  // hết [A2] → [E]
  pC.setGoToPage(pE);   // hết [B2] → [E]
  // hết [C] → [D] và hết [D] → [E]: đi theo thứ tự tự nhiên.

  var ss = SpreadsheetApp.create('Siuu — kết quả khảo sát học qua video');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Link gửi người trả lời: ' + form.getPublishedUrl());
  Logger.log('Link sửa form: ' + form.getEditUrl());
  Logger.log('Sheet kết quả: ' + ss.getUrl());
}
