import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SearchRequest {
  topic: string;
  limit?: number;
  provider?: string;
}

export interface QueryRequest {
  collection_name: string;
  question: string;
  n_results?: number;
  mode?: string;
  provider?: string;
}

export interface HistoryEntry {
  id?: string;
  collection_name: string;
  question: string;
  answer: string;
  mode: string;
  timestamp?: Date;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  searchPapers(request: SearchRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/papers/search`, request);
  }

  listCollections(): Observable<any> {
    return this.http.get(`${this.baseUrl}/papers/collections`);
  }

  deleteCollection(collectionName: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/papers/collections/${collectionName}`);
  }

  queryPapers(request: QueryRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat/query`, request);
  }

  comparePapers(request: QueryRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat/compare`, request);
  }

  generateLiteratureReview(request: QueryRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat/literature-review`, request);
  }

  identifyResearchGaps(request: QueryRequest): Observable<any> {
    return this.http.post(`${this.baseUrl}/chat/research-gaps`, request);
  }

  saveHistory(entry: HistoryEntry): Observable<any> {
    return this.http.post(`${this.baseUrl}/history/save`, entry);
  }

  getHistory(limit?: number): Observable<any> {
    const params = limit ? { limit: limit.toString() } : {};
    return this.http.get(`${this.baseUrl}/history/list`, { params });
  }

  deleteHistoryEntry(entryId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/history/${entryId}`);
  }

  clearHistory(): Observable<any> {
    return this.http.delete(`${this.baseUrl}/history/clear`);
  }
}
