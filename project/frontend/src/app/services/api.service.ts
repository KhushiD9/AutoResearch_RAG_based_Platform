import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SearchRequest   { topic: string; limit?: number; provider?: string; }
export interface QueryRequest    { collection_name: string; question: string; n_results?: number; mode?: string; provider?: string; }
export interface HistoryEntry    { id?: string; collection_name: string; question: string; answer: string; mode: string; timestamp?: Date; }

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  searchPapers(req: SearchRequest):                Observable<any> { return this.http.post(`${this.base}/papers/search`, { ...req, provider: 'anthropic' }); }
  listCollections():                               Observable<any> { return this.http.get(`${this.base}/papers/collections`); }
  deleteCollection(name: string):                  Observable<any> { return this.http.delete(`${this.base}/papers/collections/${name}`); }

  queryPapers(req: QueryRequest):                  Observable<any> { return this.http.post(`${this.base}/chat/query`, { ...req, provider: 'anthropic' }); }
  comparePapers(req: QueryRequest):                Observable<any> { return this.http.post(`${this.base}/chat/compare`, { ...req, provider: 'anthropic' }); }
  generateLiteratureReview(req: QueryRequest):     Observable<any> { return this.http.post(`${this.base}/chat/literature-review`, { ...req, provider: 'anthropic' }); }
  identifyResearchGaps(req: QueryRequest):         Observable<any> { return this.http.post(`${this.base}/chat/research-gaps`, { ...req, provider: 'anthropic' }); }

  saveHistory(entry: HistoryEntry):                Observable<any> { return this.http.post(`${this.base}/history/save`, entry); }
  getHistory(limit = 50):                          Observable<any> { return this.http.get(`${this.base}/history/list`, { params: { limit: limit.toString() } }); }
  deleteHistoryEntry(id: string):                  Observable<any> { return this.http.delete(`${this.base}/history/${id}`); }
  clearHistory():                                  Observable<any> { return this.http.delete(`${this.base}/history/clear`); }
}
