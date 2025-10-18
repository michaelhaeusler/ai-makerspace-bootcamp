'use client';

import { useState } from 'react';
import { Tab } from '@headlessui/react';
import { FileText, AlertTriangle, MessageCircle } from 'lucide-react';
import type { PolicyOverview } from '@/types';

interface PolicyTabsProps {
  policy: PolicyOverview;
  onAskQuestion: (question: string) => void;
}

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export default function PolicyTabs({ policy, onAskQuestion }: PolicyTabsProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [question, setQuestion] = useState('');

  const tabs = [
    {
      name: 'Übersicht',
      icon: FileText,
      content: (
        <div className="space-y-6">
          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Police Information
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Dateiname</dt>
                <dd className="text-sm text-gray-900">{policy.filename}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Upload-Datum</dt>
                <dd className="text-sm text-gray-900">
                  {new Date(policy.upload_date).toLocaleDateString('de-DE')}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Seitenzahl</dt>
                <dd className="text-sm text-gray-900">{policy.total_pages}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Text-Abschnitte</dt>
                <dd className="text-sm text-gray-900">{policy.total_chunks}</dd>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Schnellzugriff
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={() => onAskQuestion('Was sind meine Wartezeiten?')}
                className="text-left p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                data-testid="quick-question-waiting-periods"
              >
                <div className="font-medium text-gray-900">Wartezeiten</div>
                <div className="text-sm text-gray-500">
                  Erfahren Sie mehr über Ihre Wartezeiten
                </div>
              </button>
              <button
                onClick={() => onAskQuestion('Welche Leistungen sind ausgeschlossen?')}
                className="text-left p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                data-testid="quick-question-exclusions"
              >
                <div className="font-medium text-gray-900">Ausschlüsse</div>
                <div className="text-sm text-gray-500">
                  Welche Behandlungen sind nicht versichert?
                </div>
              </button>
              <button
                onClick={() => onAskQuestion('Wie hoch ist meine Selbstbeteiligung?')}
                className="text-left p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                data-testid="quick-question-deductible"
              >
                <div className="font-medium text-gray-900">Selbstbeteiligung</div>
                <div className="text-sm text-gray-500">
                  Ihre Kosten bei Behandlungen
                </div>
              </button>
              <button
                onClick={() => onAskQuestion('Welche Leistungen sind im Ausland versichert?')}
                className="text-left p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                data-testid="quick-question-abroad"
              >
                <div className="font-medium text-gray-900">Auslandsschutz</div>
                <div className="text-sm text-gray-500">
                  Versicherungsschutz außerhalb Deutschlands
                </div>
              </button>
            </div>
          </div>
        </div>
      )
    },
    {
      name: 'Highlights',
      icon: AlertTriangle,
      content: (
        <div className="space-y-4">
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <AlertTriangle className="w-5 h-5 text-amber-600 mr-2" />
              <h3 className="text-lg font-semibold text-amber-900">
                Ungewöhnliche Klauseln gefunden
              </h3>
            </div>
            <p className="text-amber-800 text-sm">
              Diese Klauseln weichen von typischen Branchenstandards ab und verdienen besondere Aufmerksamkeit.
            </p>
          </div>

          {policy.highlighted_clauses.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>Noch keine Highlights verfügbar.</p>
              <p className="text-sm">Die Analyse wird nach dem Upload durchgeführt.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {policy.highlighted_clauses.map((clause) => (
                <div
                  key={clause.clause_id}
                  className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
                  data-testid={`highlighted-clause-${clause.clause_id}`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="font-semibold text-gray-900">{clause.title}</h4>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      {clause.category}
                    </span>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-1">Klauseltext:</h5>
                      <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                        {clause.text}
                      </p>
                    </div>

                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-1">Warum markiert?</h5>
                      <p className="text-sm text-gray-600">{clause.reason}</p>
                    </div>

                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-1">Vergleich mit Branchenstandard:</h5>
                      <p className="text-sm text-gray-600">{clause.norm_comparison}</p>
                    </div>

                    {clause.page_number && (
                      <div className="text-xs text-gray-500">
                        Seite {clause.page_number} im Original-Dokument
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )
    },
    {
      name: 'Fragen',
      icon: MessageCircle,
      content: (
        <div className="space-y-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <MessageCircle className="w-5 h-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-blue-900">
                Fragen Sie mich alles!
              </h3>
            </div>
            <p className="text-blue-800 text-sm">
              Stellen Sie spezifische Fragen zu Ihrer Police oder allgemeine Fragen zur Krankenversicherung.
            </p>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <div className="space-y-4">
              <div>
                <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                  Ihre Frage
                </label>
                <textarea
                  id="question"
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="z.B. 'Wie lange sind meine Wartezeiten für Zahnbehandlungen?' oder 'Was bedeutet Selbstbeteiligung?'"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  data-testid="question-input"
                />
              </div>
              <button
                onClick={() => {
                  if (question.trim()) {
                    onAskQuestion(question);
                    setQuestion('');
                  }
                }}
                disabled={!question.trim()}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                data-testid="ask-question-button"
              >
                <MessageCircle className="w-4 h-4 mr-2" />
                Frage stellen
              </button>
            </div>
          </div>

          {/* Question history would go here */}
          <div className="text-center py-8 text-gray-500">
            <MessageCircle className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>Noch keine Fragen gestellt.</p>
            <p className="text-sm">Ihr Frageverlauf wird hier angezeigt.</p>
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="w-full">
      <Tab.Group selectedIndex={selectedIndex} onChange={setSelectedIndex}>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
          {tabs.map((tab, index) => (
            <Tab
              key={tab.name}
              className={({ selected }) =>
                classNames(
                  'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                  'ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                  selected
                    ? 'bg-white text-blue-700 shadow'
                    : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                )
              }
              data-testid={`tab-${tab.name.toLowerCase()}`}
            >
              <div className="flex items-center justify-center space-x-2">
                <tab.icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </div>
            </Tab>
          ))}
        </Tab.List>
        <Tab.Panels className="mt-6">
          {tabs.map((tab, tabIndex) => (
            <Tab.Panel
              key={tabIndex}
              className={classNames(
                'rounded-xl bg-white p-6',
                'ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2'
              )}
            >
              {tab.content}
            </Tab.Panel>
          ))}
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
}
