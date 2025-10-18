'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import PolicyTabs from '@/components/PolicyTabs';
import type { PolicyUploadResponse, PolicyOverview } from '@/types';

export default function Home() {
  const [uploadedPolicy, setUploadedPolicy] = useState<PolicyOverview | null>(null);

  const handleUploadComplete = (result: PolicyUploadResponse) => {
    // Convert upload response to policy overview format
    const policyOverview: PolicyOverview = {
      policy_id: result.policy_id,
      filename: result.filename,
      upload_date: new Date().toISOString(),
      total_pages: 0, // Will be populated after backend processing
      total_chunks: result.total_chunks,
      highlighted_clauses: result.highlights.map((highlight, index) => ({
        clause_id: `clause-${index}-${Date.now()}`,
        title: typeof highlight === 'object' && highlight && 'title' in highlight ? String(highlight.title) : 'Unbenannte Klausel',
        text: typeof highlight === 'object' && highlight && 'text' in highlight ? String(highlight.text) : '',
        reason: typeof highlight === 'object' && highlight && 'reason' in highlight ? String(highlight.reason) : '',
        norm_comparison: typeof highlight === 'object' && highlight && 'norm_comparison' in highlight ? String(highlight.norm_comparison) : '',
        category: typeof highlight === 'object' && highlight && 'category' in highlight ? String(highlight.category) : 'other',
        page_number: typeof highlight === 'object' && highlight && 'page_number' in highlight && typeof highlight.page_number === 'number' ? highlight.page_number : undefined,
      })),
    };

    setUploadedPolicy(policyOverview);
  };

  const handleAskQuestion = async (question: string) => {
    if (!uploadedPolicy) return;

    console.log('Asking question:', question, 'for policy:', uploadedPolicy.policy_id);
    // TODO: Implement actual question handling with backend API
    // This will be connected to the backend in the next phase
  };

  const handleStartOver = () => {
    setUploadedPolicy(null);
  };

  return (
    <div className="space-y-8">
      {!uploadedPolicy ? (
        <div className="text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Willkommen bei InsuranceLens
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Laden Sie Ihre deutsche Krankenversicherungs-Police hoch und erhalten Sie
              eine KI-gestützte Analyse mit personalisierten Antworten auf Ihre Fragen.
            </p>
          </div>

          <FileUpload onUploadComplete={handleUploadComplete} />

          <div className="bg-blue-50 rounded-lg p-6 max-w-4xl mx-auto">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">
              Was macht InsuranceLens?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              <div className="space-y-2">
                <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">1</span>
                </div>
                <h3 className="font-semibold text-blue-900">Analyse</h3>
                <p className="text-blue-800 text-sm">
                  Ihre Police wird analysiert und mit Branchenstandards verglichen
                </p>
              </div>
              <div className="space-y-2">
                <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">2</span>
                </div>
                <h3 className="font-semibold text-blue-900">Highlights</h3>
                <p className="text-blue-800 text-sm">
                  Ungewöhnliche Klauseln werden identifiziert und erklärt
                </p>
              </div>
              <div className="space-y-2">
                <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">3</span>
                </div>
                <h3 className="font-semibold text-blue-900">Fragen</h3>
                <p className="text-blue-800 text-sm">
                  Stellen Sie Fragen und erhalten Sie präzise Antworten mit Quellenangaben
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Police: {uploadedPolicy.filename}
              </h1>
              <p className="text-gray-600">
                Hochgeladen am {new Date(uploadedPolicy.upload_date).toLocaleDateString('de-DE')}
              </p>
            </div>
            <button
              onClick={handleStartOver}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              data-testid="start-over-button"
            >
              Neue Police hochladen
            </button>
          </div>

          <PolicyTabs
            policy={uploadedPolicy}
            onAskQuestion={handleAskQuestion}
          />
        </div>
      )}
    </div>
  );
}