'use client';

import { useState } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { api } from '@/utils/api';
import type { PolicyUploadResponse, UploadProgress } from '@/types';

interface FileUploadProps {
  onUploadComplete: (result: PolicyUploadResponse) => void;
}

export default function FileUpload({ onUploadComplete }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState<UploadProgress>({
    stage: 'uploading',
    progress: 0,
    message: 'Bereit zum Upload...'
  });
  const [error, setError] = useState<string | null>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFile = async (file: File) => {
    if (!file.type.includes('pdf')) {
      setError('Bitte wählen Sie eine PDF-Datei aus.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
      setError('Die Datei ist zu groß. Maximum: 50MB');
      return;
    }

    setError(null);
    setUploading(true);
    
    try {
      setProgress({
        stage: 'uploading',
        progress: 0,
        message: 'Upload läuft...'
      });

      const result = await api.uploadPolicy(file, (uploadProgress) => {
        setProgress({
          stage: 'uploading',
          progress: uploadProgress,
          message: `Upload: ${Math.round(uploadProgress)}%`
        });
      });

      setProgress({
        stage: 'processing',
        progress: 90,
        message: 'Verarbeitung läuft...'
      });

      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 2000));

      setProgress({
        stage: 'complete',
        progress: 100,
        message: 'Upload erfolgreich!'
      });

      onUploadComplete(result);
      
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Upload fehlgeschlagen';
      setError(errorMessage);
      setProgress({
        stage: 'uploading',
        progress: 0,
        message: 'Bereit zum Upload...'
      });
    } finally {
      setUploading(false);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-400 bg-blue-50'
            : error
            ? 'border-red-300 bg-red-50'
            : 'border-gray-300 bg-white hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {uploading ? (
          <div className="space-y-4">
            <div className="flex justify-center">
              {progress.stage === 'complete' ? (
                <CheckCircle className="w-12 h-12 text-green-500" />
              ) : (
                <FileText className="w-12 h-12 text-blue-500 animate-pulse" />
              )}
            </div>
            <div className="space-y-2">
              <div className="text-lg font-medium text-gray-900">
                {progress.message}
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress.progress}%` }}
                ></div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex justify-center">
              {error ? (
                <AlertCircle className="w-12 h-12 text-red-500" />
              ) : (
                <Upload className="w-12 h-12 text-gray-400" />
              )}
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Krankenversicherungs-Police hochladen
              </h3>
              <p className="text-gray-600 mb-4">
                Ziehen Sie Ihre PDF-Datei hier hinein oder klicken Sie zum Auswählen
              </p>
              {error && (
                <p className="text-red-600 text-sm mb-4">{error}</p>
              )}
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileInput}
                className="hidden"
                id="file-upload"
                data-testid="file-upload-input"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer transition-colors"
                data-testid="file-upload-button"
              >
                <Upload className="w-4 h-4 mr-2" />
                PDF auswählen
              </label>
            </div>
            <p className="text-xs text-gray-500">
              Nur PDF-Dateien, max. 50MB. Ihre Daten werden privat und sicher verarbeitet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
