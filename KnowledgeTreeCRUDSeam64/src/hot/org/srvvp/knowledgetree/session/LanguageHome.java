package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("languageHome")
public class LanguageHome extends EntityHome<Language> {

	public void setLanguageId(String id) {
		setId(id);
	}

	public String getLanguageId() {
		return (String) getId();
	}

	@Override
	protected Language createInstance() {
		Language language = new Language();
		return language;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Language getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<WorkInLanguage> getWorkInLanguages() {
		return getInstance() == null ? null : new ArrayList<WorkInLanguage>(
				getInstance().getWorkInLanguages());
	}

}
