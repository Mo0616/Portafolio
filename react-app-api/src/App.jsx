import { useEffect, useMemo, useState } from 'react';

const fallbackQuestions = [
  {
    question: 'Que hook de React se usa para manejar estado local?',
    correct_answer: 'useState',
    incorrect_answers: ['useEffect', 'useMemo', 'useRef']
  },
  {
    question: 'Que metodo HTTP se usa normalmente para consultar datos?',
    correct_answer: 'GET',
    incorrect_answers: ['POST', 'PATCH', 'DELETE']
  },
  {
    question: 'Que formato se usa con frecuencia para responder desde una API REST?',
    correct_answer: 'JSON',
    incorrect_answers: ['XLSX', 'PNG', 'MP3']
  }
];

function decodeHtml(value) {
  const element = document.createElement('textarea');
  element.innerHTML = value;
  return element.value;
}

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
}

export default function App() {
  const [questions, setQuestions] = useState(fallbackQuestions);
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [selected, setSelected] = useState('');
  const [status, setStatus] = useState('Cargando preguntas...');

  useEffect(() => {
    async function loadQuestions() {
      try {
        const response = await fetch('https://opentdb.com/api.php?amount=5&type=multiple');
        const data = await response.json();
        if (!data.results?.length) {
          throw new Error('Respuesta vacia');
        }
        setQuestions(data.results);
        setStatus('Preguntas cargadas desde la API.');
      } catch {
        setStatus('Modo local activo con preguntas de respaldo.');
      }
    }

    loadQuestions();
  }, []);

  const question = questions[current];
  const answers = useMemo(
    () => shuffle([question.correct_answer, ...question.incorrect_answers]),
    [question]
  );
  const finished = current >= questions.length - 1 && selected;

  function chooseAnswer(answer) {
    if (selected) {
      return;
    }

    setSelected(answer);
    if (answer === question.correct_answer) {
      setScore((value) => value + 1);
    }
  }

  function nextQuestion() {
    setSelected('');
    setCurrent((value) => Math.min(value + 1, questions.length - 1));
  }

  function restart() {
    setCurrent(0);
    setScore(0);
    setSelected('');
  }

  return (
    <main className="screen">
      <section className="game-panel">
        <div className="game-copy">
          <p className="eyebrow">Diana Quest</p>
          <h1>Responde, suma puntos y avanza.</h1>
          <p>{status}</p>
        </div>

        <div className="question-zone">
          <div className="progress">
            <span>Pregunta {current + 1} de {questions.length}</span>
            <strong>{score} puntos</strong>
          </div>

          <h2>{decodeHtml(question.question)}</h2>

          <div className="answers">
            {answers.map((answer) => {
              const isCorrect = selected && answer === question.correct_answer;
              const isWrong = selected === answer && answer !== question.correct_answer;
              return (
                <button
                  className={isCorrect ? 'correct' : isWrong ? 'wrong' : ''}
                  key={answer}
                  onClick={() => chooseAnswer(answer)}
                  type="button"
                >
                  {decodeHtml(answer)}
                </button>
              );
            })}
          </div>

          {selected && (
            <div className="feedback">
              <p>{selected === question.correct_answer ? 'Respuesta correcta.' : 'Respuesta incorrecta.'}</p>
              {finished ? (
                <button type="button" onClick={restart}>Reiniciar partida</button>
              ) : (
                <button type="button" onClick={nextQuestion}>Siguiente</button>
              )}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
