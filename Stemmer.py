from konlpy.tag import Komoran
komoran = Komoran()

print(komoran.morphs(u'우왕 코모란도 오픈소스가 되었어요'))
print(komoran.nouns(u'오픈소스에 관심 많은 멋진 개발자님들!'))
print(komoran.pos(u'한글형태소분석기 코모란 테스트 중 입니다.'))

# 오류 내용
# Traceback (most recent call last): ...

# 오류 해결
# 시스템 환경 변수 > JAVA_HOME 경로 다시 확인