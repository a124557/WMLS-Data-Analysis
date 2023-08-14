import config
import analyzeLimeSurvey
import analyzeSymmSpan
import analyzeNBack
import write


analyzeLimeSurvey.analyzeLimeSurvey(config.limeSurveyFile)
analyzeSymmSpan.analyzeSymmSpan()
analyzeNBack.analyzeNBack()
write.write()
