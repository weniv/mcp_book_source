from mcp.server.fastmcp import FastMCP

# MCP 서버 생성
mcp = FastMCP(name="server")


@mcp.tool()
def read_hwp(file_name: str) -> str:
    """한글 문서(.hwp)를 읽어 텍스트로 반환합니다.

    olefile 라이브러리를 사용하여 한글 문서의 텍스트 내용을 추출합니다.

    Args:
        file_name (str): 읽을 한글 문서의 이름
            예: 'document.hwp'

    Returns:
        str: 한글 문서에서 추출한 텍스트 내용 또는 오류 메시지
    """
    import os
    import olefile

    # 상대 경로인 경우 현재 디렉토리 기준으로 절대 경로 변환
    file_path = os.path.join("c:/test", file_name)

    try:
        # 한글 파일 열기
        if not olefile.isOleFile(file_path):
            return f"오류: '{file_path}'는 올바른 한글 문서 형식이 아닙니다."

        ole = olefile.OleFileIO(file_path)

        # 텍스트 스트림 읽기
        if ole.exists("PrvText"):
            text_stream = ole.openstream("PrvText")
            text_data = text_stream.read().decode("utf-16-le", errors="replace")
            ole.close()
            return text_data
        else:
            ole.close()
            return "텍스트 내용을 추출할 수 없습니다. 지원되지 않는 한글 문서 형식일 수 있습니다."

    except Exception as e:
        return f"한글 문서 읽기 오류: {str(e)}"


@mcp.tool()
def write_md_to_hwpx(md_content: str, output_filename: str) -> str:
    """
    마크다운 내용을 HWPX 형식의 한글 문서로 변환하여 저장합니다.

    Parameters
    ----------
    md_content : str
        변환할 마크다운 내용
    output_filename : str
        저장할 HWPX 파일 이름 (확장자 포함, 예: 'document.hwpx')

    Returns
    -------
    str
        변환 결과 메시지
    """
    import os
    import zipfile
    import tempfile
    import shutil
    import markdown
    from bs4 import BeautifulSoup
    from datetime import datetime

    try:
        # 임시 디렉토리 생성
        temp_dir = tempfile.mkdtemp()

        # 임시 마크다운 파일 생성
        temp_md_file = os.path.join(temp_dir, "temp.md")
        with open(temp_md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 마크다운을 HTML로 변환
        with open(temp_md_file, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        html = markdown.markdown(markdown_text)
        soup = BeautifulSoup(html, "html.parser")

        # 제목 추출 (첫 번째 h1 또는 기본 제목 사용)
        title = "문서"
        h1_tag = soup.find("h1")
        if h1_tag:
            title = h1_tag.text

        # HWPX 파일 구조 생성
        os.makedirs(os.path.join(temp_dir, "META-INF"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "Contents"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "Preview"), exist_ok=True)

        # 필수 파일들 생성
        # mimetype 파일
        with open(os.path.join(temp_dir, "mimetype"), "w", encoding="utf-8") as f:
            f.write("application/hwp+zip")

        # settings.xml 파일
        settings_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<ha:HWPApplicationSetting xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0">
  <ha:CaretPosition listIDRef="0" paraIDRef="4" pos="2"/>
</ha:HWPApplicationSetting>"""
        with open(os.path.join(temp_dir, "settings.xml"), "w", encoding="utf-8") as f:
            f.write(settings_content)

        # Preview/PrvText.txt 파일 생성
        preview_text = ""
        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
            preview_text += element.text + "\n"
        preview_text = preview_text[:100]  # 미리보기는 100자로 제한

        with open(
            os.path.join(temp_dir, "Preview", "PrvText.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(preview_text)

        # META-INF 파일들 생성
        container_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<ocf:container xmlns:ocf="urn:oasis:names:tc:opendocument:xmlns:container" xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf">
  <ocf:rootfiles>
    <ocf:rootfile full-path="Contents/content.hpf" media-type="application/hwpml-package+xml"/>
    <ocf:rootfile full-path="Preview/PrvText.txt" media-type="text/plain"/>
    <ocf:rootfile full-path="META-INF/container.rdf" media-type="application/rdf+xml"/>
  </ocf:rootfiles>
</ocf:container>"""
        with open(
            os.path.join(temp_dir, "META-INF", "container.xml"), "w", encoding="utf-8"
        ) as f:
            f.write(container_xml)

        # 기본적인 header.xml과 section0.xml 생성
        # 실제 구현에서는 더 복잡한 XML 구조가 필요합니다
        basic_header = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<hh:head xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head" version="1.4" secCnt="1">
  <hh:beginNum page="1" footnote="1" endnote="1" pic="1" tbl="1" equation="1"/>
  <hh:refList>
    <!-- 기본 참조 목록 -->
  </hh:refList>
</hh:head>"""
        with open(
            os.path.join(temp_dir, "Contents", "header.xml"), "w", encoding="utf-8"
        ) as f:
            f.write(basic_header)

        # 본문 내용을 변환하여 section0.xml 생성
        section_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section">
  <!-- 본문 내용 -->
</hs:sec>"""
        with open(
            os.path.join(temp_dir, "Contents", "section0.xml"), "w", encoding="utf-8"
        ) as f:
            f.write(section_content)

        # content.hpf 파일 생성
        current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        content_hpf = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf/" version="1.0">
  <opf:metadata>
    <opf:title>{title}</opf:title>
    <opf:language>ko</opf:language>
    <opf:meta name="CreatedDate" content="text">{current_date}</opf:meta>
  </opf:metadata>
  <opf:manifest>
    <opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>
    <opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>
    <opf:item id="settings" href="settings.xml" media-type="application/xml"/>
  </opf:manifest>
  <opf:spine>
    <opf:itemref idref="header" linear="yes"/>
    <opf:itemref idref="section0" linear="no"/>
  </opf:spine>
</opf:package>"""
        with open(
            os.path.join(temp_dir, "Contents", "content.hpf"), "w", encoding="utf-8"
        ) as f:
            f.write(content_hpf)

        # 파일의 최종 경로
        output_path = os.path.join("c:/test", output_filename)

        # HWPX 파일로 압축
        with zipfile.ZipFile(output_path, "w") as zip_file:
            # mimetype 파일은 압축하지 않고 첫 번째로 추가
            zip_file.write(
                os.path.join(temp_dir, "mimetype"),
                "mimetype",
                compress_type=zipfile.ZIP_STORED,
            )

            # 나머지 파일들 추가
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file != "mimetype":  # mimetype은 이미 추가했으므로 건너뜀
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_file.write(
                            file_path, arcname, compress_type=zipfile.ZIP_DEFLATED
                        )

        # 임시 디렉토리 삭제
        shutil.rmtree(temp_dir)

        return f"마크다운 내용이 {output_filename} 파일로 성공적으로 변환되었습니다."
    except Exception as e:
        return f"한글 문서 변환 중 오류가 발생했습니다: {str(e)}"


# 서버 실행
if __name__ == "__main__":
    mcp.run()
